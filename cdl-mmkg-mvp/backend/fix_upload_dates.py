"""
Fix upload_date for migrated documents
Set current datetime for documents with null upload_date
"""

import asyncio
from datetime import datetime
from core.database import database


async def fix_upload_dates():
    """Add proper upload dates to documents that have null values"""
    print("=" * 60)
    print("Fixing Upload Dates")
    print("=" * 60)
    
    try:
        # Connect to database
        print("\n1. Connecting to database...")
        await database.connect()
        print("✅ Database connected successfully")
        
        collection = database.client.cdl_mvp.documents
        
        # Count documents with null upload_date
        null_date_count = await collection.count_documents({"upload_date": None})
        print(f"\n2. Found {null_date_count} documents with null upload_date")
        
        if null_date_count == 0:
            print("✅ All documents have valid upload_date")
            return
        
        # Update documents with null upload_date
        print("\n3. Setting upload_date to current datetime...")
        current_time = datetime.utcnow()
        
        result = await collection.update_many(
            {"upload_date": None},
            {"$set": {"upload_date": current_time}}
        )
        
        print(f"✅ Updated {result.modified_count} documents with upload_date: {current_time.isoformat()}")
        
        # Verify fix
        print("\n4. Verifying fix...")
        null_count = await collection.count_documents({"upload_date": None})
        valid_count = await collection.count_documents({"upload_date": {"$ne": None}})
        
        print(f"  - Documents with null upload_date: {null_count}")
        print(f"  - Documents with valid upload_date: {valid_count}")
        
        # Show sample document
        print("\n5. Sample document after fix:")
        doc = await collection.find_one({})
        if doc:
            print(f"  ID: {doc.get('_id')}")
            print(f"  Title: {doc.get('title', 'N/A')}")
            print(f"  Upload Date: {doc.get('upload_date')}")
            print(f"  Upload Date Type: {type(doc.get('upload_date'))}")
        
        print("\n" + "=" * 60)
        print("✅ Upload dates fixed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Fix failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Disconnect
        print("\n6. Closing connection...")
        await database.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    asyncio.run(fix_upload_dates())
