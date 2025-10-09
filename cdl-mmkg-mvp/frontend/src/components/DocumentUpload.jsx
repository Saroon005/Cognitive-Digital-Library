import { useState } from 'react';
import { uploadDocument } from '../services/api';
import './DocumentUpload.css';

function DocumentUpload({ onUploadSuccess }) {
  const [formData, setFormData] = useState({
    title: '',
    authors: '',
    tags: '',
  });
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
      'text/plain'
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setError('Please upload a PDF, DOCX, or TXT file');
      setFile(null);
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) { // 10MB limit
      setError('File size must be less than 10MB');
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError(null);
    
    // Auto-fill title if empty
    if (!formData.title) {
      const fileName = selectedFile.name.replace(/\.[^/.]+$/, ''); // Remove extension
      setFormData(prev => ({ ...prev, title: fileName }));
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    if (!formData.title.trim()) {
      setError('Please enter a title');
      return;
    }

    setIsUploading(true);

    try {
      const uploadFormData = new FormData();
      uploadFormData.append('file', file);
      uploadFormData.append('title', formData.title.trim());
      uploadFormData.append('authors', formData.authors.trim());
      uploadFormData.append('tags', formData.tags.trim());

      const result = await uploadDocument(uploadFormData);
      
      setSuccess(true);
      setFormData({ title: '', authors: '', tags: '' });
      setFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('file-input');
      if (fileInput) fileInput.value = '';

      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }

      // Auto-hide success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);

    } catch (err) {
      setError(err.message || 'Failed to upload document');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>📤 Upload Document</h2>
      
      <form onSubmit={handleSubmit} className="upload-form">
        {/* File Drop Zone */}
        <div
          className={`drop-zone ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-input"
            onChange={handleFileChange}
            accept=".pdf,.docx,.doc,.txt"
            className="file-input"
          />
          
          {!file ? (
            <>
              <div className="upload-icon">📁</div>
              <p className="drop-text">
                Drag & drop your document here, or{' '}
                <label htmlFor="file-input" className="browse-link">
                  browse
                </label>
              </p>
              <p className="file-types">Supported: PDF, DOCX, TXT (Max 10MB)</p>
            </>
          ) : (
            <div className="file-selected">
              <div className="file-icon">📄</div>
              <div className="file-info">
                <p className="file-name">{file.name}</p>
                <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
              </div>
              <button
                type="button"
                onClick={() => {
                  setFile(null);
                  const fileInput = document.getElementById('file-input');
                  if (fileInput) fileInput.value = '';
                }}
                className="remove-file-btn"
              >
                ✕
              </button>
            </div>
          )}
        </div>

        {/* Form Fields */}
        <div className="form-group">
          <label htmlFor="title">
            Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            placeholder="Enter document title"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="authors">Authors</label>
          <input
            type="text"
            id="authors"
            name="authors"
            value={formData.authors}
            onChange={handleInputChange}
            placeholder="Enter authors (comma-separated)"
          />
          <small>Example: John Doe, Jane Smith</small>
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleInputChange}
            placeholder="Enter tags (comma-separated)"
          />
          <small>Example: AI, Machine Learning, Research</small>
        </div>

        {/* Messages */}
        {error && (
          <div className="alert alert-error">
            ⚠️ {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            ✅ Document uploaded successfully!
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isUploading || !file}
          className="submit-btn"
        >
          {isUploading ? (
            <>
              <span className="spinner"></span>
              Uploading...
            </>
          ) : (
            <>
              <span>📤</span>
              Upload Document
            </>
          )}
        </button>
      </form>
    </div>
  );
}

export default DocumentUpload;
