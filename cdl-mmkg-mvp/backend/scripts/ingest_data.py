import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from core.database import database
from services.nlp_service import nlp_service


async def main():
    sample_documents = [
        "Artificial intelligence is transforming the way we interact with technology and solve complex problems.",
        "Machine learning algorithms can identify patterns in large datasets to make accurate predictions.",
        "Data science combines statistics, programming, and domain expertise to extract insights from data.",
        "Natural language processing enables computers to understand and generate human language effectively."
    ]
    
    await database.connect()
    collection = database.client.cdl_mvp.documents
    
    for doc_text in sample_documents:
        embedding = nlp_service.generate_embedding(doc_text)
        document = {
            "text": doc_text,
            "abstract_embedding": embedding
        }
        await collection.insert_one(document)
    
    print("Successfully ingested sample documents with embeddings")
    await database.close()


asyncio.run(main())
