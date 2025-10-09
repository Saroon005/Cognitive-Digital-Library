# 📐 Project Setup Flow & Architecture

## 🔄 Setup Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        PREREQUISITES                            │
│  ✓ Python 3.10+    ✓ Node.js 16+    ✓ MongoDB Atlas Account   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    MONGODB ATLAS SETUP                          │
│  1. Create Account → 2. Create Cluster → 3. Add User            │
│  4. Whitelist IP → 5. Get Connection String                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
        ┌───────────────────┐ ┌───────────────────┐
        │  BACKEND SETUP    │ │  FRONTEND SETUP   │
        │                   │ │                   │
        │ 1. Create venv    │ │ 1. Navigate to    │
        │ 2. Activate venv  │ │    frontend dir   │
        │ 3. pip install -r │ │ 2. npm install    │
        │    requirements   │ │                   │
        │ 4. Create .env    │ │                   │
        │ 5. Add MONGO_URI  │ │                   │
        └───────────────────┘ └───────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │           RUN APPLICATION               │
        │                                         │
        │  Terminal 1:        Terminal 2:         │
        │  (Backend)          (Frontend)          │
        │                                         │
        │  python main.py     npm run dev         │
        │                                         │
        │  Port 8000          Port 5173           │
        └─────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │    ACCESS: http://localhost:5173        │
        └─────────────────────────────────────────┘
```

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                            USER BROWSER                            │
│                      http://localhost:5173                         │
└────────────────────────────────────────────────────────────────────┘
                                 ↕
                        HTTP Requests/Responses
                                 ↕
┌────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  Search Tab  │  │  Upload Tab  │  │  Manage Tab  │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              API Service (Axios)                         │    │
│  │  - searchDocuments()   - uploadDocument()                │    │
│  │  - getAllDocuments()   - updateDocument()                │    │
│  │  - deleteDocument()                                      │    │
│  └──────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
                                 ↕
                    REST API (JSON over HTTP)
                                 ↕
┌────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI + Python)                      │
│                      http://localhost:8000                         │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    API Endpoints                            │ │
│  │  /search/          - Semantic search                        │ │
│  │  /documents/       - Get all documents                      │ │
│  │  /documents/{id}   - Get/Update/Delete single document     │ │
│  │  /documents/upload - Upload new document                   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                ↕                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Services Layer                           │ │
│  │                                                             │ │
│  │  NLP Service                  File Processor                │ │
│  │  ├─ Load Model                ├─ Extract PDF               │ │
│  │  ├─ Generate Embeddings       ├─ Extract DOCX              │ │
│  │  └─ Calculate Similarity      └─ Extract TXT               │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                ↕                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Data Models (Pydantic)                   │ │
│  │  - DocumentCreate   - DocumentResponse                      │ │
│  │  - DocumentUpdate   - DocumentSearchResponse                │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
                                 ↕
                     MongoDB Driver (Motor - Async)
                                 ↕
┌────────────────────────────────────────────────────────────────────┐
│                      MongoDB Atlas (Cloud)                         │
│                                                                    │
│  Database: cdl_mvp                                                │
│  Collection: documents                                            │
│                                                                    │
│  Document Schema:                                                 │
│  {                                                                │
│    "_id": "ObjectId",                                             │
│    "title": "string",                                             │
│    "content": "string",              // Extracted text            │
│    "content_embedding": [float...],  // 384 dimensions            │
│    "authors": ["string"],                                         │
│    "tags": ["string"],                                            │
│    "file_path": "string",            // Local file path           │
│    "metadata": {                     // File metadata             │
│      "original_filename": "string",                               │
│      "file_size": number,                                         │
│      "file_type": "string"                                        │
│    },                                                             │
│    "upload_date": "datetime"                                      │
│  }                                                                │
└────────────────────────────────────────────────────────────────────┘
                                 ↕
┌────────────────────────────────────────────────────────────────────┐
│                     Local File System                              │
│                   backend/uploads/                                 │
│  - document1.pdf                                                  │
│  - document2.docx                                                 │
│  - document3.txt                                                  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Request Flow Example: Document Upload

```
1. USER ACTION
   ↓ [User selects file and clicks "Upload"]
   
2. FRONTEND (React Component)
   ↓ File → FormData → Axios POST request
   
3. HTTP REQUEST
   ↓ POST /documents/upload
   ↓ Content-Type: multipart/form-data
   ↓ Body: {file, title, authors, tags}
   
4. BACKEND (FastAPI)
   ↓ Receive file upload
   
5. FILE PROCESSOR
   ↓ Determine file type (PDF/DOCX/TXT)
   ↓ Extract text content
   ↓ Save file to uploads/ directory
   
6. NLP SERVICE
   ↓ Generate embedding from content
   ↓ [Sentence Transformer Model]
   ↓ Returns 384-dimensional vector
   
7. DATABASE OPERATION
   ↓ Create document object with:
   ↓ - Content
   ↓ - Embedding
   ↓ - Metadata
   ↓ Insert into MongoDB
   
8. RESPONSE
   ↓ Return document ID and details
   ↓ HTTP 200 OK
   
9. FRONTEND UPDATE
   ↓ Show success message
   ↓ Refresh document list
   
10. USER FEEDBACK
    ✅ "Document uploaded successfully!"
```

---

## 🔎 Request Flow Example: Semantic Search

```
1. USER ACTION
   ↓ [User enters "machine learning" and clicks Search]
   
2. FRONTEND (React Component)
   ↓ Query → Axios GET request
   
3. HTTP REQUEST
   ↓ GET /search/?query=machine+learning&limit=10
   
4. BACKEND (FastAPI)
   ↓ Receive search query
   
5. NLP SERVICE
   ↓ Generate embedding for query "machine learning"
   ↓ [Sentence Transformer Model]
   ↓ Returns 384-dimensional query vector
   
6. DATABASE OPERATION - Try Vector Search
   ↓ MongoDB $vectorSearch (if index exists)
   ↓ Compare query vector with document embeddings
   ↓ Calculate cosine similarity
   
   [If vector search fails]
   ↓ FALLBACK: Regex text search
   ↓ Search in title and content fields
   ↓ Manual similarity calculation
   
7. RANKING
   ↓ Sort results by similarity score
   ↓ Apply limit (default 10)
   
8. RESPONSE
   ↓ Return list of matching documents
   ↓ Each with similarity score
   ↓ HTTP 200 OK
   
9. FRONTEND UPDATE
   ↓ Display results in cards
   ↓ Show relevance scores
   ↓ Highlight matched content
   
10. USER SEES RESULTS
    📊 Ranked documents by relevance
```

---

## 💾 Data Flow: Document Storage

```
Document Lifecycle:
═══════════════════

UPLOAD
  ↓
  File (PDF/DOCX/TXT)
  ↓
  TEXT EXTRACTION
  ├─ PDF: PyPDF2
  ├─ DOCX: python-docx
  └─ TXT: Direct read
  ↓
  Extracted Text
  ↓
  EMBEDDING GENERATION
  [Sentence Transformer]
  ↓
  384-dimensional vector
  ↓
  STORAGE (Parallel)
  ├─ File → uploads/ folder
  └─ Metadata + Embedding → MongoDB
  ↓
  Document Stored ✓

RETRIEVAL
  ↓
  Database Query
  ↓
  Document Metadata
  ↓
  File Reference (file_path)
  ↓
  Display in UI

UPDATE
  ↓
  Modified Metadata
  ↓
  [If content changed]
  → Regenerate Embedding
  ↓
  Update in MongoDB

DELETE
  ↓
  Delete from MongoDB
  ↓
  Delete file from uploads/
  ↓
  Document Removed ✓
```

---

## 🔐 Security & Configuration Flow

```
Environment Variables (.env)
═══════════════════════════
  ↓
Backend Startup
  ↓
Config Loader (pydantic-settings)
  ↓
┌─────────────────────────────┐
│ Configuration Object        │
│                             │
│ - MONGO_URI (MongoDB)       │
│ - DATABASE_NAME             │
│ - COLLECTION_NAME           │
│ - PORT                      │
│ - CORS_ORIGINS              │
│ - HOST                      │
└─────────────────────────────┘
  ↓
Used throughout application
  ↓
Never exposed to frontend
```

---

## 🧩 Component Interaction Map

```
FRONTEND COMPONENTS
═══════════════════

App.jsx (Main Container)
  │
  ├─── SearchBar.jsx
  │     ├─ Input field
  │     ├─ Search button
  │     └─ API: searchDocuments()
  │
  ├─── ResultList.jsx
  │     ├─ Display search results
  │     ├─ Show relevance scores
  │     └─ Expandable content
  │
  ├─── DocumentUpload.jsx
  │     ├─ File input (drag-drop)
  │     ├─ Form fields (title, authors, tags)
  │     ├─ Upload button
  │     └─ API: uploadDocument()
  │
  └─── DocumentManagement.jsx
        ├─ Document list (grid)
        ├─ Edit functionality
        ├─ Delete functionality
        ├─ Filter/search
        ├─ API: getAllDocuments()
        ├─ API: updateDocument()
        └─ API: deleteDocument()

                ↕
           API Service Layer
                ↕
      Backend API Endpoints
```

---

## 📊 Performance Optimization Flow

```
OPTIMIZATION STRATEGIES
═══════════════════════

1. EMBEDDING CACHING
   - Generate once on upload
   - Store in database
   - Reuse for all searches
   
2. PAGINATION
   - Default limit: 100 documents
   - Skip/Limit parameters
   - Reduces data transfer
   
3. PROJECTION
   - Exclude embeddings from list views
   - Include only necessary fields
   - Faster queries
   
4. ASYNC OPERATIONS
   - Non-blocking I/O
   - Concurrent request handling
   - Motor async driver
   
5. INDEX USAGE
   - MongoDB indexes on common fields
   - Vector search index (optional)
   - Faster query execution
   
6. FILE STREAMING
   - Stream large files
   - Chunked upload
   - Memory efficient
```

---

## 🔄 Development Workflow

```
┌─────────────────────────────────────────────────┐
│          DEVELOPMENT WORKFLOW                   │
└─────────────────────────────────────────────────┘

Day-to-Day Development:
  1. Start Backend (Terminal 1)
     cd backend → activate venv → python main.py
     
  2. Start Frontend (Terminal 2)
     cd frontend → npm run dev
     
  3. Open Browser
     http://localhost:5173
     
  4. Make Changes
     - Backend: Auto-reloads (uvicorn --reload)
     - Frontend: Hot Module Replacement (HMR)
     
  5. Test Changes
     - Manual testing in browser
     - API testing in /docs
     
  6. Stop Servers
     Ctrl+C in both terminals

Git Workflow:
  1. Create feature branch
  2. Make changes
  3. Test locally
  4. Commit changes
  5. Push to GitHub
  6. Create pull request

Deployment:
  1. Backend → Cloud provider (AWS, GCP, Heroku)
  2. Frontend → Static hosting (Vercel, Netlify)
  3. Update CORS settings
  4. Use production MongoDB cluster
```

---

## 🎯 Key Integration Points

```
Integration Points:
═══════════════════

1. Frontend ↔ Backend
   - REST API over HTTP
   - JSON data format
   - CORS enabled
   - Port: 8000

2. Backend ↔ MongoDB
   - Motor async driver
   - Connection pool
   - Authentication via URI
   
3. Backend ↔ File System
   - Local uploads/ directory
   - File path references in DB
   - Async file operations
   
4. Backend ↔ ML Model
   - Sentence Transformers
   - One-time model loading
   - GPU support (optional)
   
5. Frontend ↔ Browser
   - Single Page Application
   - Client-side routing
   - Local state management
```

This architecture ensures scalability, maintainability, and clear separation of concerns! 🚀
