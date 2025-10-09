"""
Migration script to update old document schema to new schema
This will rename 'text' to 'content' and 'abstract_embedding' to 'content_embedding'
"""

import asyncio
from core.database import database


async def migrate_documents():
    """Migrate old document schema to new schema"""
    print("=" * 60)
    print("Migrating Document Schema")
    print("=" * 60)
    
    try:
        # Connect to database
        print("\n1. Connecting to database...")
        await database.connect()
        print("✅ Database connected successfully")
        
        collection = database.client.cdl_mvp.documents
        
        # Count documents with old schema
        old_schema_count = await collection.count_documents({"text": {"$exists": True}})
        print(f"\n2. Found {old_schema_count} documents with old schema")
        
        if old_schema_count == 0:
            print("✅ No documents need migration")
            return
        
        # Migrate documents
        print("\n3. Migrating documents...")
        
        # Rename 'text' to 'content'
        result1 = await collection.update_many(
            {"text": {"$exists": True}},
            {"$rename": {"text": "content"}}
        )
        print(f"  - Renamed 'text' to 'content': {result1.modified_count} documents")
        
        # Rename 'abstract_embedding' to 'content_embedding'
        result2 = await collection.update_many(
            {"abstract_embedding": {"$exists": True}},
            {"$rename": {"abstract_embedding": "content_embedding"}}
        )
        print(f"  - Renamed 'abstract_embedding' to 'content_embedding': {result2.modified_count} documents")
        
        # Add missing fields with defaults
        result3 = await collection.update_many(
            {"title": {"$exists": False}},
            {"$set": {"title": "Untitled Document"}}
        )
        print(f"  - Added missing 'title' field: {result3.modified_count} documents")
        
        result4 = await collection.update_many(
            {"authors": {"$exists": False}},
            {"$set": {"authors": []}}
        )
        print(f"  - Added missing 'authors' field: {result4.modified_count} documents")
        
        result5 = await collection.update_many(
            {"tags": {"$exists": False}},
            {"$set": {"tags": []}}
        )
        print(f"  - Added missing 'tags' field: {result5.modified_count} documents")
        
        result6 = await collection.update_many(
            {"upload_date": {"$exists": False}},
            {"$set": {"upload_date": None}}
        )
        print(f"  - Added missing 'upload_date' field: {result6.modified_count} documents")
        
        # Verify migration
        print("\n4. Verifying migration...")
        old_count = await collection.count_documents({"text": {"$exists": True}})
        new_count = await collection.count_documents({"content": {"$exists": True}})
        
        print(f"  - Documents with old 'text' field: {old_count}")
        print(f"  - Documents with new 'content' field: {new_count}")
        
        if old_count == 0:
            print("\n✅ Migration completed successfully!")
        else:
            print(f"\n⚠️  Warning: {old_count} documents still have old schema")
        
        # Show sample document
        print("\n5. Sample migrated document:")
        doc = await collection.find_one({})
        if doc:
            print(f"  ID: {doc.get('_id')}")
            print(f"  Title: {doc.get('title', 'N/A')}")
            print(f"  Has content: {'content' in doc}")
            print(f"  Has content_embedding: {'content_embedding' in doc}")
            print(f"  Authors: {doc.get('authors', [])}")
            print(f"  Tags: {doc.get('tags', [])}")
            print(f"  Upload Date: {doc.get('upload_date', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("✅ Migration completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Disconnect
        print("\n6. Closing connection...")
        await database.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    asyncio.run(migrate_documents())
