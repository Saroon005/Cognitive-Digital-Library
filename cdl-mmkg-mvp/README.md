# Cognitive Digital Library - Enhanced MVP

An advanced document management system with AI-powered semantic search, CRUD operations, and file upload capabilities.

## 🌟 Features

### Core Functionality
- **Semantic Search**: AI-powered vector search using sentence transformers for intelligent document retrieval
- **Document Upload**: Support for PDF, DOCX, and TXT file uploads with automatic text extraction
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for documents
- **Rich Metadata**: Store and manage document titles, authors, tags, and custom metadata
- **Modern UI**: Beautiful, responsive interface with gradient designs and smooth animations

### Technical Features
- **FastAPI Backend**: High-performance async API with automatic documentation
- **MongoDB Atlas**: Cloud-based NoSQL database with vector search capabilities
- **React Frontend**: Modern, component-based UI with tabbed navigation
- **File Processing**: Automatic text extraction from various file formats
- **Error Handling**: Comprehensive error handling and user feedback

## 📁 Project Structure

```
cdl-mmkg-mvp/
├── backend/
│   ├── main.py                 # Main FastAPI application (run this!)
│   ├── requirements.txt        # Python dependencies
│   ├── api/
│   │   ├── search.py          # Search endpoints
│   │   └── documents.py       # CRUD endpoints
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── database.py        # Database connection
│   ├── models/
│   │   └── document.py        # Pydantic models
│   ├── services/
│   │   ├── nlp_service.py     # NLP/embedding service
│   │   └── file_processor.py  # File extraction utilities
│   └── uploads/               # Uploaded files storage
└── frontend/
    ├── src/
    │   ├── App.jsx            # Main app with tabs
    │   ├── components/
    │   │   ├── SearchBar.jsx          # Search interface
    │   │   ├── ResultList.jsx         # Search results display
    │   │   ├── DocumentUpload.jsx     # File upload form
    │   │   └── DocumentManagement.jsx # Document list & edit
    │   └── services/
    │       └── api.jsx        # API service layer
    └── package.json
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- MongoDB Atlas account (free tier works)

### Backend Setup

1. **Navigate to backend directory**:
   ```powershell
   cd cdl-mmkg-mvp/backend
   ```

2. **Create virtual environment** (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Create `.env` file** in `backend/` directory:
   ```env
   MONGO_URI=your_mongodb_atlas_connection_string
   ```

5. **Run the backend server**:
   ```powershell
   python main.py
   ```
   
   The server will start on `http://localhost:8000`
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Frontend Setup

1. **Navigate to frontend directory**:
   ```powershell
   cd cdl-mmkg-mvp/frontend
   ```

2. **Install dependencies**:
   ```powershell
   npm install
   ```

3. **Start development server**:
   ```powershell
   npm run dev
   ```
   
   The app will open at `http://localhost:5173`

## 📚 API Endpoints

### Search
- `GET /search/?q={query}&limit={limit}` - Semantic search across documents

### Documents CRUD
- `POST /documents/` - Create document (JSON)
- `POST /documents/upload` - Upload document file
- `GET /documents/` - List all documents (with optional filtering)
- `GET /documents/{id}` - Get specific document
- `PUT /documents/{id}` - Update document
- `DELETE /documents/{id}` - Delete document

### System
- `GET /` - API info
- `GET /health` - Health check

## 🎨 User Interface

The application features three main tabs:

### 1. Search Tab 🔍
- Semantic search bar with auto-suggestions
- Beautiful result cards with relevance scores
- Display of document metadata (title, authors, tags)
- Expandable content previews

### 2. Upload Tab 📤
- Drag-and-drop file upload interface
- Support for PDF, DOCX, TXT files (max 10MB)
- Form fields for title, authors, and tags
- Real-time file validation
- Success notifications

### 3. Manage Tab 📚
- Grid view of all documents
- Filter by tags
- Inline editing capabilities
- Delete confirmation dialogs
- Document metadata display
- Responsive card layout

## 🔧 Configuration

### Backend Configuration (`backend/core/config.py`)
- MongoDB connection string
- Environment variables handling
- Application settings

### Frontend Configuration
- API base URL in `frontend/src/services/api.jsx`
- Default set to `http://localhost:8000`

## 📦 Dependencies

### Backend
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **motor**: Async MongoDB driver
- **sentence-transformers**: Embeddings generation
- **spacy**: NLP processing
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **python-multipart**: File upload handling
- **pydantic-settings**: Configuration management

### Frontend
- **react**: UI framework
- **axios**: HTTP client
- **vite**: Build tool and dev server

## 🎯 Usage Examples

### Uploading a Document
1. Click the "Upload" tab
2. Drag and drop a PDF/DOCX/TXT file
3. Enter document title (auto-filled from filename)
4. Add authors (comma-separated)
5. Add tags (comma-separated)
6. Click "Upload Document"

### Searching Documents
1. Click the "Search" tab
2. Enter your search query in natural language
3. Press "Search" or hit Enter
4. View results sorted by relevance

### Managing Documents
1. Click the "Manage" tab
2. View all uploaded documents
3. Use filter to find specific tags
4. Click edit (✏️) to modify a document
5. Click delete (🗑️) to remove a document

## 🔒 Security Notes

- The `.env` file is not committed to Git
- Virtual environments are excluded from version control
- CORS is configured for local development only
- File uploads are validated for type and size
- MongoDB connection uses secure connection strings

## 🐛 Troubleshooting

### Backend Issues
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Database connection fails**: Check your MongoDB Atlas connection string in `.env`
- **Port already in use**: Stop other services on port 8000 or change in `main.py`

### Frontend Issues
- **API connection fails**: Ensure backend is running on port 8000
- **Build errors**: Delete `node_modules` and run `npm install` again
- **CORS errors**: Check that frontend URL is in backend CORS allowed origins

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Document versioning
- [ ] Advanced filtering and sorting
- [ ] Document sharing and collaboration
- [ ] Export functionality
- [ ] Batch operations
- [ ] Analytics dashboard
- [ ] Document previews
- [ ] Multi-language support

## 🤝 Contributing

This is an educational project. Feel free to fork and enhance!

## 📄 License

MIT License - feel free to use for learning and development.

---

**Cognitive Digital Library v2.0** - Built with ❤️ using FastAPI, React, and MongoDB
