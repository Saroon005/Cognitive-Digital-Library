from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from models.document import (
    DocumentCreate, 
    DocumentUpdate, 
    DocumentResponse,
    DocumentInDB
)
from core.database import database
from services.nlp_service import nlp_service
from bson import ObjectId
from datetime import datetime
import os
import shutil

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/debug/count")
async def debug_document_count():
    """Debug endpoint to check document count and sample data"""
    collection = database.client.cdl_mvp.documents
    
    try:
        count = await collection.count_documents({})
        
        # Get one sample document
        sample = await collection.find_one({})
        if sample:
            sample["_id"] = str(sample["_id"])
            # Remove embedding for readability
            if "content_embedding" in sample:
                sample["content_embedding"] = f"Array of {len(sample['content_embedding'])} values"
        
        return {
            "total_documents": count,
            "sample_document": sample,
            "collection_name": "cdl_mvp.documents"
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to connect to database"
        }


@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(document: DocumentCreate):
    """Create a new document without file upload"""
    collection = database.client.cdl_mvp.documents
    
    # Generate embedding for content
    embedding = nlp_service.generate_embedding(document.content)
    
    document_dict = document.model_dump()
    document_dict["upload_date"] = datetime.utcnow()
    document_dict["content_embedding"] = embedding
    
    result = await collection.insert_one(document_dict)
    
    created_doc = await collection.find_one({"_id": result.inserted_id})
    created_doc["_id"] = str(created_doc["_id"])
    
    return created_doc


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    authors: str = Form(""),
    tags: str = Form("")
):
    """Upload a document file (PDF, DOCX, TXT) and extract content"""
    collection = database.client.cdl_mvp.documents
    
    # Validate file type
    allowed_extensions = [".pdf", ".docx", ".txt", ".doc"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract content based on file type
    try:
        if file_ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif file_ext == ".pdf":
            from services.file_processor import extract_text_from_pdf
            content = extract_text_from_pdf(file_path)
        elif file_ext in [".docx", ".doc"]:
            from services.file_processor import extract_text_from_docx
            content = extract_text_from_docx(file_path)
    except Exception as e:
        # Clean up file if extraction fails
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
    
    if not content or len(content.strip()) < 10:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="No readable content found in file")
    
    # Parse authors and tags
    authors_list = [a.strip() for a in authors.split(",") if a.strip()] if authors else []
    tags_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    
    # Generate embedding
    embedding = nlp_service.generate_embedding(content[:5000])  # Limit to first 5000 chars
    
    document_dict = {
        "title": title,
        "content": content,
        "authors": authors_list,
        "tags": tags_list,
        "file_path": file_path,
        "metadata": {
            "original_filename": file.filename,
            "file_size": os.path.getsize(file_path),
            "file_type": file_ext
        },
        "upload_date": datetime.utcnow(),
        "content_embedding": embedding
    }
    
    result = await collection.insert_one(document_dict)
    
    created_doc = await collection.find_one({"_id": result.inserted_id})
    created_doc["_id"] = str(created_doc["_id"])
    
    return created_doc


@router.get("/", response_model=List[DocumentResponse])
async def get_all_documents(skip: int = 0, limit: int = 50, tags: Optional[str] = None):
    """Retrieve all documents with optional filtering by tags"""
    collection = database.client.cdl_mvp.documents
    
    try:
        query = {}
        if tags:
            tag_list = [t.strip() for t in tags.split(",")]
            query["tags"] = {"$in": tag_list}
        
        # Exclude content_embedding from response for performance
        projection = {
            "_id": 1,
            "title": 1,
            "content": 1,
            "authors": 1,
            "tags": 1,
            "file_path": 1,
            "metadata": 1,
            "upload_date": 1
        }
        
        cursor = collection.find(query, projection).sort("upload_date", -1).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        
        return documents
    except Exception as e:
        print(f"Error fetching documents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Retrieve a specific document by ID"""
    collection = database.client.cdl_mvp.documents
    
    try:
        doc = await collection.find_one({"_id": ObjectId(document_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc["_id"] = str(doc["_id"])
    return doc


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: str, document: DocumentUpdate):
    """Update a document"""
    collection = database.client.cdl_mvp.documents
    
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    
    # Check if document exists
    existing = await collection.find_one({"_id": obj_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Build update dict (only include non-None fields)
    update_data = {k: v for k, v in document.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # If content is updated, regenerate embedding
    if "content" in update_data:
        update_data["content_embedding"] = nlp_service.generate_embedding(update_data["content"])
    
    # Update document
    await collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    
    # Fetch and return updated document
    updated_doc = await collection.find_one({"_id": obj_id})
    updated_doc["_id"] = str(updated_doc["_id"])
    
    return updated_doc


@router.delete("/{document_id}", status_code=204)
async def delete_document(document_id: str):
    """Delete a document"""
    collection = database.client.cdl_mvp.documents
    
    try:
        obj_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    
    # Check if document exists and get file_path
    doc = await collection.find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete the physical file if it exists
    if doc.get("file_path") and os.path.exists(doc["file_path"]):
        try:
            os.remove(doc["file_path"])
        except Exception as e:
            print(f"Warning: Could not delete file {doc['file_path']}: {e}")
    
    # Delete from database
    result = await collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return None
