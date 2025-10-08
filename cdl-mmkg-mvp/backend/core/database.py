import motor.motor_asyncio
from core.config import settings


class Database:
    def __init__(self):
        self.client = None
    
    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
        print("Connected to MongoDB")
    
    async def close(self):
        self.client.close()
        print("Closed MongoDB connection")


database = Database()
