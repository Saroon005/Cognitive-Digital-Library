from fastapi import APIRouter
from typing import List
from models.document import DocumentResponse
from core.database import database
from services.nlp_service import nlp_service

router = APIRouter()


@router.get("/search", response_model=List[DocumentResponse])
async def search(q: str):
    collection = database.client.cdl_mvp.documents
    
    query_embedding = nlp_service.generate_embedding(q)
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "abstract_embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 10
            }
        },
        {
            "$project": {
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
                "_id": 0
            }
        }
    ]
    
    results = await collection.aggregate(pipeline).to_list(length=10)
    return results
