import { useState, useEffect } from 'react';
import { getAllDocuments, deleteDocument, updateDocument } from '../services/api';
import './DocumentManagement.css';

function DocumentManagement({ refreshTrigger }) {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [filterTag, setFilterTag] = useState('');

  useEffect(() => {
    loadDocuments();
  }, [refreshTrigger]);

  const loadDocuments = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAllDocuments(0, 100, filterTag || null);
      setDocuments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (documentId, title) => {
    if (!confirm(`Are you sure you want to delete "${title}"?`)) {
      return;
    }

    try {
      await deleteDocument(documentId);
      setDocuments(documents.filter(doc => doc._id !== documentId));
    } catch (err) {
      alert(`Failed to delete: ${err.message}`);
    }
  };

  const startEdit = (doc) => {
    setEditingId(doc._id);
    setEditForm({
      title: doc.title,
      authors: doc.authors.join(', '),
      tags: doc.tags.join(', '),
      content: doc.content
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditForm({});
  };

  const saveEdit = async (documentId) => {
    try {
      const updateData = {
        title: editForm.title,
        authors: editForm.authors.split(',').map(a => a.trim()).filter(a => a),
        tags: editForm.tags.split(',').map(t => t.trim()).filter(t => t),
        content: editForm.content
      };

      const updated = await updateDocument(documentId, updateData);
      setDocuments(documents.map(doc => doc._id === documentId ? updated : doc));
      setEditingId(null);
      setEditForm({});
    } catch (err) {
      alert(`Failed to update: ${err.message}`);
    }
  };

  const handleFilterChange = (e) => {
    setFilterTag(e.target.value);
  };

  const applyFilter = () => {
    loadDocuments();
  };

  const truncateText = (text, maxLength = 200) => {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="management-container">
        <div className="loading-state">
          <div className="spinner-large"></div>
          <p>Loading documents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="management-container">
      <div className="management-header">
        <h2>📚 Manage Documents</h2>
        <div className="filter-section">
          <input
            type="text"
            placeholder="Filter by tags (comma-separated)"
            value={filterTag}
            onChange={handleFilterChange}
            className="filter-input"
          />
          <button onClick={applyFilter} className="filter-btn">
            🔍 Filter
          </button>
          <button onClick={loadDocuments} className="refresh-btn">
            🔄 Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          ⚠️ {error}
        </div>
      )}

      {documents.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📭</div>
          <p>No documents found</p>
          <small>Upload your first document to get started</small>
        </div>
      ) : (
        <div className="documents-grid">
          {documents.map(doc => (
            <div key={doc._id} className="document-card">
              {editingId === doc._id ? (
                /* Edit Mode */
                <div className="edit-form">
                  <input
                    type="text"
                    value={editForm.title}
                    onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                    className="edit-input"
                    placeholder="Title"
                  />
                  <input
                    type="text"
                    value={editForm.authors}
                    onChange={(e) => setEditForm({...editForm, authors: e.target.value})}
                    className="edit-input"
                    placeholder="Authors (comma-separated)"
                  />
                  <input
                    type="text"
                    value={editForm.tags}
                    onChange={(e) => setEditForm({...editForm, tags: e.target.value})}
                    className="edit-input"
                    placeholder="Tags (comma-separated)"
                  />
                  <textarea
                    value={editForm.content}
                    onChange={(e) => setEditForm({...editForm, content: e.target.value})}
                    className="edit-textarea"
                    placeholder="Content"
                    rows="6"
                  />
                  <div className="edit-actions">
                    <button onClick={() => saveEdit(doc._id)} className="btn-save">
                      ✓ Save
                    </button>
                    <button onClick={cancelEdit} className="btn-cancel">
                      ✕ Cancel
                    </button>
                  </div>
                </div>
              ) : (
                /* View Mode */
                <>
                  <div className="card-header">
                    <h3>{doc.title}</h3>
                    <div className="card-actions">
                      <button
                        onClick={() => startEdit(doc)}
                        className="btn-icon btn-edit"
                        title="Edit"
                      >
                        ✏️
                      </button>
                      <button
                        onClick={() => handleDelete(doc._id, doc.title)}
                        className="btn-icon btn-delete"
                        title="Delete"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>

                  {doc.authors && doc.authors.length > 0 && (
                    <div className="card-meta">
                      <span className="meta-label">👤 Authors:</span>
                      <span className="meta-value">{doc.authors.join(', ')}</span>
                    </div>
                  )}

                  {doc.tags && doc.tags.length > 0 && (
                    <div className="card-tags">
                      {doc.tags.map((tag, idx) => (
                        <span key={idx} className="tag">{tag}</span>
                      ))}
                    </div>
                  )}

                  <div className="card-content">
                    {truncateText(doc.content)}
                  </div>

                  {doc.metadata && doc.metadata.original_filename && (
                    <div className="card-meta">
                      <span className="meta-label">📄 File:</span>
                      <span className="meta-value">{doc.metadata.original_filename}</span>
                    </div>
                  )}

                  <div className="card-footer">
                    <small>📅 {formatDate(doc.upload_date)}</small>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="documents-count">
        Total: {documents.length} document{documents.length !== 1 ? 's' : ''}
      </div>
    </div>
  );
}

export default DocumentManagement;
