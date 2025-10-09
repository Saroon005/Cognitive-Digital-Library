# 🚀 Quick Start Guide - Cognitive Digital Library

## ⚡ Fast Setup (5 Minutes)

### Prerequisites Check
```bash
python --version    # Should be 3.10+
node --version      # Should be 16+
npm --version       # Should be 8+
```

---

## 📝 Setup Steps

### 1️⃣ MongoDB Atlas Setup
1. Sign up: https://www.mongodb.com/cloud/atlas/register
2. Create free M0 cluster
3. Add database user (save username/password!)
4. Allow all IPs in Network Access
5. Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/`

### 2️⃣ Backend Setup

```powershell
# Navigate to backend
cd cdl-mmkg-mvp/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1        # Windows PowerShell
# OR
venv\Scripts\activate.bat          # Windows CMD
# OR
source venv/bin/activate           # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Add your MongoDB URI (see below)
```

**.env file content:**
```env
MONGO_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=cdl_mvp
COLLECTION_NAME=documents
PORT=8000
```

### 3️⃣ Frontend Setup (NEW TERMINAL!)

```bash
# Open NEW terminal window
cd cdl-mmkg-mvp/frontend

# Install dependencies
npm install
```

---

## 🎯 Running the Application

### Terminal 1 - Backend
```powershell
cd cdl-mmkg-mvp/backend
.\venv\Scripts\Activate.ps1    # Activate venv
python main.py                 # Start server
```
**Backend runs on:** http://localhost:8000

### Terminal 2 - Frontend  
```bash
cd cdl-mmkg-mvp/frontend
npm run dev                    # Start dev server
```
**Frontend runs on:** http://localhost:5173

---

## ✅ Verify It Works

1. **Open browser:** http://localhost:5173
2. **See three tabs:** Search, Upload, Manage
3. **Upload a document** (PDF/DOCX/TXT)
4. **Search for it**
5. **View in Manage tab**

---

## 🐛 Common Issues

### Backend won't start
```bash
# Make sure venv is activated (you should see "(venv)" in prompt)
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

### Can't connect to MongoDB
1. Check .env file has correct MongoDB URI
2. Verify IP is whitelisted in MongoDB Atlas
3. Test connection: `python test_connection.py`

### Port already in use
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
# In .env: PORT=8001
```

---

## 📚 Key URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application |
| Backend API | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive docs |
| Health Check | http://localhost:8000/health | Server status |

---

## 🎓 First Time Tips

1. **Two Terminals Required:**
   - Terminal 1: Backend (stays running)
   - Terminal 2: Frontend (stays running)

2. **Virtual Environment:**
   - Always activate before running backend
   - Look for `(venv)` in command prompt

3. **Test Connection:**
   - Run `python test_connection.py` before starting server
   - Should show: "✅ All tests passed!"

4. **Upload Test Document:**
   - Start with a small TXT file
   - Then try PDF/DOCX
   - Check `uploads/` folder for stored files

5. **API Documentation:**
   - Visit http://localhost:8000/docs
   - Test endpoints directly in browser
   - See request/response formats

---

## 🔄 Daily Workflow

### Starting Work
```bash
# Terminal 1
cd cdl-mmkg-mvp/backend
.\venv\Scripts\Activate.ps1
python main.py

# Terminal 2 (new window)
cd cdl-mmkg-mvp/frontend
npm run dev
```

### Stopping
```bash
# In both terminals:
Ctrl + C
```

---

## 📖 Feature Overview

### Search Tab
- Enter query, get ranked results
- Uses AI to understand meaning
- Shows relevance scores

### Upload Tab
- Drag-and-drop or click to browse
- Add title, authors, tags
- Supports PDF, DOCX, TXT

### Manage Tab
- View all documents
- Edit metadata inline
- Delete documents
- Filter by title

---

## 💡 Pro Tips

1. **Database Inspection:**
   ```bash
   python test_connection.py
   ```

2. **Check Logs:**
   - Backend: Terminal shows all requests
   - Frontend: Browser DevTools Console (F12)

3. **Clear Cache:**
   - Browser: Ctrl+Shift+R
   - Backend: Restart server
   - Frontend: `npm run dev` again

4. **File Location:**
   - Uploads: `backend/uploads/`
   - Config: `backend/.env`
   - Database: MongoDB Atlas dashboard

5. **API Testing:**
   - Use http://localhost:8000/docs
   - Or Postman/Insomnia
   - Or curl commands

---

## 🎯 Success Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 16+ installed
- [ ] MongoDB Atlas account created
- [ ] Cluster created and running
- [ ] Database user added
- [ ] IP whitelisted
- [ ] Connection string copied
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] .env file created with MongoDB URI
- [ ] Frontend dependencies installed
- [ ] Backend server starts successfully
- [ ] Frontend server starts successfully
- [ ] Can access http://localhost:5173
- [ ] Can upload a document
- [ ] Can search documents
- [ ] Can view documents in Manage tab

---

## 🆘 Need Help?

1. Read full README.md for detailed explanations
2. Check TROUBLESHOOTING.md for common issues
3. Visit http://localhost:8000/docs for API reference
4. Review terminal error messages carefully
5. Verify .env file configuration
6. Test MongoDB connection separately

---

**Ready? Let's go! 🚀**

Run backend → Run frontend → Open browser → Start uploading!
