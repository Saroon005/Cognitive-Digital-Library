from fastapi import APIRouter, Query, HTTPException
from typing import List
from models.document import DocumentSearchResponse
from core.database import database
from services.nlp_service import nlp_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=List[DocumentSearchResponse])
async def search_documents(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return")
):
    """
    Semantic search across documents using vector similarity
    Falls back to text search if vector index is not available
    """
    collection = database.client.cdl_mvp.documents
    
    # Generate embedding for the search query
    query_embedding = nlp_service.generate_embedding(q)
    
    # Try vector search first (requires Atlas vector index)
    try:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "content_embedding",
                    "queryVector": query_embedding,
                    "numCandidates": limit * 10,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "title": 1,
                    "content": {"$substr": ["$content", 0, 500]},
                    "authors": 1,
                    "tags": 1,
                    "upload_date": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        results = await collection.aggregate(pipeline).to_list(length=limit)
        
        # If vector search returns results, return them
        if results:
            print(f"Vector search returned {len(results)} results")
            return results
        
    except Exception as e:
        print(f"Vector search not available: {e}")
    
    # Fallback: Use text search with manual similarity calculation
    print(f"Using text search fallback for query: {q}")
    
    try:
        # Text-based search with regex
        cursor = collection.find(
            {
                "$or": [
                    {"title": {"$regex": q, "$options": "i"}},
                    {"content": {"$regex": q, "$options": "i"}},
                    {"tags": {"$in": [{"$regex": q, "$options": "i"}]}}
                ]
            },
            {
                "_id": 1,
                "title": 1,
                "content": 1,
                "authors": 1,
                "tags": 1,
                "upload_date": 1,
                "content_embedding": 1
            }
        ).limit(limit * 2)  # Get more candidates for scoring
        
        docs = await cursor.to_list(length=limit * 2)
        
        if not docs:
            print("No documents found with text search")
            return []
        
        # Calculate similarity scores manually
        results = []
        for doc in docs:
            # Calculate cosine similarity if embeddings exist
            score = 0.5  # default score
            if "content_embedding" in doc and doc["content_embedding"]:
                try:
                    # Simple dot product for similarity (normalized embeddings)
                    doc_embedding = doc["content_embedding"]
                    if len(doc_embedding) == len(query_embedding):
                        score = sum(a * b for a, b in zip(query_embedding, doc_embedding))
                        score = max(0, min(1, (score + 1) / 2))  # Normalize to 0-1
                except Exception as e:
                    print(f"Error calculating similarity: {e}")
            
            results.append({
                "_id": str(doc["_id"]),
                "title": doc.get("title", ""),
                "content": doc.get("content", "")[:500],
                "authors": doc.get("authors", []),
                "tags": doc.get("tags", []),
                "upload_date": doc.get("upload_date"),
                "score": score
            })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        print(f"Text search returned {len(results[:limit])} results")
        return results[:limit]
        
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
