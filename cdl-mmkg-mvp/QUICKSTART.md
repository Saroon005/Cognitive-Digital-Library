# Quick Start Guide - Cognitive Digital Library

## 🚀 5-Minute Setup

### Step 1: Install Backend Dependencies
```powershell
cd cdl-mmkg-mvp\backend
pip install -r requirements.txt
```

### Step 2: Configure Environment
Create `backend\.env` file:
```env
MONGO_URI=your_mongodb_atlas_connection_string
```

### Step 3: Install Frontend Dependencies
```powershell
cd ..\frontend
npm install
```

### Step 4: Start Backend Server
```powershell
cd ..\backend
python main.py
```
✅ Backend running at http://localhost:8000

### Step 5: Start Frontend (New Terminal)
```powershell
cd cdl-mmkg-mvp\frontend
npm run dev
```
✅ Frontend running at http://localhost:5173

## 🎯 First Steps

### 1. Upload Your First Document
- Click **Upload** tab
- Drag & drop a PDF/DOCX/TXT file
- Fill in title, authors, tags
- Click **Upload Document**

### 2. Search for Documents
- Click **Search** tab
- Enter a search query
- View semantic search results

### 3. Manage Documents
- Click **Manage** tab
- View all documents
- Edit or delete documents

## ⚡ Quick Commands

### Backend Only
```powershell
cd cdl-mmkg-mvp\backend
python main.py
```

### Frontend Only
```powershell
cd cdl-mmkg-mvp\frontend
npm run dev
```

### Install All Dependencies
```powershell
# Backend
cd cdl-mmkg-mvp\backend
pip install -r requirements.txt

# Frontend
cd ..\frontend
npm install
```

## 🔗 Important URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## ⚠️ Common Issues

### Backend won't start?
- Check Python version: `python --version` (need 3.8+)
- Verify `.env` file exists with valid MONGO_URI
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start?
- Check Node version: `node --version` (need 16+)
- Install dependencies: `npm install`
- Delete `node_modules` and reinstall if issues persist

### Can't upload files?
- Check backend is running on port 8000
- Verify file is PDF, DOCX, or TXT (max 10MB)
- Check browser console for errors

### Search not working?
- Ensure MongoDB Atlas vector index is created
- Check backend logs for errors
- Verify documents are uploaded with embeddings

## 📚 Test Data

Upload these sample documents to test:
1. **Research Paper** (PDF)
2. **Meeting Notes** (DOCX)
3. **Code Documentation** (TXT)

## 🎓 Next Steps

1. ✅ Upload 5-10 documents
2. ✅ Test semantic search with different queries
3. ✅ Try editing a document
4. ✅ Test filtering by tags
5. ✅ Explore the API documentation

## 💡 Pro Tips

- Use **descriptive titles** for better organization
- Add **relevant tags** for easier filtering
- Include **author names** for attribution
- Try **semantic searches** like "how to implement authentication"
- Use the **edit feature** to update content without re-uploading

---

**Ready to explore? Start with the Upload tab! 🚀**
