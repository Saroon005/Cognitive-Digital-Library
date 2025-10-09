from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.database import database
from api.search import router as search_router
from api.documents import router as documents_router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Cognitive Digital Library API...")
    await database.connect()
    print("✅ Database connected successfully")
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    print("✅ Uploads directory ready")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    await database.close()
    print("✅ Database connection closed")


app = FastAPI(
    title="Cognitive Digital Library API",
    description="Advanced document management system with semantic search capabilities",
    version="2.0.0",
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files for uploaded documents
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API routers
app.include_router(search_router)
app.include_router(documents_router)


@app.get("/", tags=["root"])
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to Cognitive Digital Library API",
        "version": "2.0.0",
        "endpoints": {
            "search": "/search?q=query",
            "documents": "/documents",
            "upload": "/documents/upload",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        await database.client.admin.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🎓 COGNITIVE DIGITAL LIBRARY - Backend Server")
    print("="*60)
    print("\n📚 Starting server...")
    print("🌐 API Documentation: http://localhost:8000/docs")
    print("🔍 Search endpoint: http://localhost:8000/search")
    print("📄 Documents endpoint: http://localhost:8000/documents")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
