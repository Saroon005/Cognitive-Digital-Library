"""
Test script to verify MongoDB connection and data fetching
Run this from the backend directory: python test_connection.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.database import database
from bson import ObjectId


async def test_connection():
    """Test MongoDB connection and document retrieval"""
    print("=" * 60)
    print("Testing MongoDB Connection and Data Fetching")
    print("=" * 60)
    
    try:
        # Connect to database
        print("\n1. Connecting to database...")
        await database.connect()
        print("✅ Database connected successfully")
        
        # Test ping
        print("\n2. Testing database ping...")
        result = await database.client.admin.command('ping')
        print(f"✅ Ping successful: {result}")
        
        # Get collection
        collection = database.client.cdl_mvp.documents
        
        # Count documents
        print("\n3. Counting documents...")
        count = await collection.count_documents({})
        print(f"✅ Found {count} documents in collection")
        
        if count == 0:
            print("⚠️  No documents found. Please upload some documents first.")
            return
        
        # Get one document
        print("\n4. Fetching sample document...")
        doc = await collection.find_one({})
        
        if doc:
            print(f"✅ Successfully retrieved document")
            print(f"\nDocument Details:")
            print(f"  ID: {doc['_id']}")
            print(f"  Title: {doc.get('title', 'N/A')}")
            print(f"  Authors: {doc.get('authors', [])}")
            print(f"  Tags: {doc.get('tags', [])}")
            print(f"  Upload Date: {doc.get('upload_date', 'N/A')}")
            print(f"  Content Length: {len(doc.get('content', ''))} characters")
            print(f"  Has Embedding: {'content_embedding' in doc}")
            if 'content_embedding' in doc:
                print(f"  Embedding Length: {len(doc['content_embedding'])}")
            print(f"  File Path: {doc.get('file_path', 'N/A')}")
            
            # Print metadata
            if 'metadata' in doc:
                print(f"\n  Metadata:")
                for key, value in doc['metadata'].items():
                    print(f"    - {key}: {value}")
        
        # List all document titles
        print("\n5. Listing all documents...")
        cursor = collection.find({}, {"_id": 1, "title": 1, "upload_date": 1})
        docs = await cursor.to_list(length=100)
        
        print(f"\nAll Documents ({len(docs)}):")
        for i, doc in enumerate(docs, 1):
            print(f"  {i}. {doc.get('title', 'Untitled')} (ID: {doc['_id']})")
        
        # Test search query
        print("\n6. Testing text search...")
        search_term = "quality"
        cursor = collection.find(
            {"$or": [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"content": {"$regex": search_term, "$options": "i"}}
            ]},
            {"_id": 1, "title": 1}
        ).limit(5)
        
        results = await cursor.to_list(length=5)
        print(f"✅ Text search for '{search_term}' found {len(results)} results")
        for doc in results:
            print(f"  - {doc.get('title', 'Untitled')}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! Database is working correctly.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\nFull error details:")
        import traceback
        traceback.print_exc()
    
    finally:
        # Disconnect
        print("\n7. Closing connection...")
        await database.close()
        print("✅ Connection closed")


async def test_specific_document(doc_id: str):
    """Test fetching a specific document by ID"""
    print(f"\nTesting specific document: {doc_id}")
    
    try:
        await database.connect()
        collection = database.client.cdl_mvp.documents
        
        doc = await collection.find_one({"_id": ObjectId(doc_id)})
        
        if doc:
            print("✅ Document found!")
            print(f"Title: {doc.get('title')}")
            print(f"Content preview: {doc.get('content', '')[:200]}...")
        else:
            print("❌ Document not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await database.close()


if __name__ == "__main__":
    # Run basic tests
    asyncio.run(test_connection())
    
    # Optionally test specific document
    # Replace with your document ID from MongoDB
    # asyncio.run(test_specific_document("68e759e6e5fa0f6e4a4eda42"))
