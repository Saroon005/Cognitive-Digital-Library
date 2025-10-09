"""
Test script to verify search functionality
Run this to test if search is working correctly
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.database import database
from services.nlp_service import nlp_service


async def test_search():
    """Test search functionality"""
    print("=" * 60)
    print("Testing Search Functionality")
    print("=" * 60)
    
    try:
        # Connect to database
        print("\n1. Connecting to database...")
        await database.connect()
        print("✅ Database connected successfully")
        
        collection = database.client.cdl_mvp.documents
        
        # Count documents
        count = await collection.count_documents({})
        print(f"\n2. Found {count} documents in collection")
        
        if count == 0:
            print("⚠️  No documents to search. Please upload some documents first.")
            return
        
        # Test query
        test_query = "quality"
        print(f"\n3. Testing search with query: '{test_query}'")
        
        # Generate embedding
        print("   - Generating query embedding...")
        query_embedding = nlp_service.generate_embedding(test_query)
        print(f"   - Embedding generated: {len(query_embedding)} dimensions")
        
        # Try vector search first
        print("\n4. Attempting vector search...")
        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "content_embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 100,
                        "limit": 10
                    }
                },
                {
                    "$project": {
                        "_id": {"$toString": "$_id"},
                        "title": 1,
                        "content": {"$substr": ["$content", 0, 200]},
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = await collection.aggregate(pipeline).to_list(length=10)
            
            if results:
                print(f"✅ Vector search successful! Found {len(results)} results")
                for i, result in enumerate(results, 1):
                    print(f"\n   Result {i}:")
                    print(f"   - Title: {result.get('title', 'N/A')}")
                    print(f"   - Score: {result.get('score', 0):.4f}")
                    print(f"   - Content: {result.get('content', 'N/A')[:100]}...")
                return
            else:
                print("⚠️  Vector search returned no results")
                
        except Exception as e:
            print(f"⚠️  Vector search failed: {e}")
            print("   This is expected if MongoDB Atlas vector index is not configured")
        
        # Test text search fallback
        print("\n5. Testing text search fallback...")
        try:
            cursor = collection.find(
                {
                    "$or": [
                        {"title": {"$regex": test_query, "$options": "i"}},
                        {"content": {"$regex": test_query, "$options": "i"}},
                        {"tags": {"$regex": test_query, "$options": "i"}},
                        {"authors": {"$regex": test_query, "$options": "i"}}
                    ]
                },
                {
                    "_id": 1,
                    "title": 1,
                    "content": 1,
                    "authors": 1,
                    "tags": 1,
                    "content_embedding": 1
                }
            ).limit(10)
            
            docs = await cursor.to_list(length=10)
            
            if docs:
                print(f"✅ Text search successful! Found {len(docs)} results")
                
                # Calculate similarity scores
                results = []
                for doc in docs:
                    score = 0.5
                    if "content_embedding" in doc and doc["content_embedding"]:
                        try:
                            doc_embedding = doc["content_embedding"]
                            if len(doc_embedding) == len(query_embedding):
                                score = sum(a * b for a, b in zip(query_embedding, doc_embedding))
                                score = max(0, min(1, (score + 1) / 2))
                        except:
                            pass
                    
                    results.append({
                        "title": doc.get("title", "N/A"),
                        "score": score,
                        "content": doc.get("content", "")[:100]
                    })
                
                results.sort(key=lambda x: x["score"], reverse=True)
                
                print("\n   Top Results:")
                for i, result in enumerate(results[:5], 1):
                    print(f"\n   Result {i}:")
                    print(f"   - Title: {result['title']}")
                    print(f"   - Score: {result['score']:.4f}")
                    print(f"   - Content: {result['content']}...")
                
            else:
                print("⚠️  No results found for the query")
                
        except Exception as e:
            print(f"❌ Text search failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("✅ Search test completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Disconnect
        print("\n6. Closing connection...")
        await database.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    asyncio.run(test_search())
