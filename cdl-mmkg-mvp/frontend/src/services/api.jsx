import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Search API
export async function searchAPI(query) {
    try {
        const response = await api.get('/search/', {
            params: { q: query, limit: 20 }
        });
        return response.data;
    } catch (error) {
        console.error('Search API error:', error);
        throw new Error(error.response?.data?.detail || 'Failed to fetch search results');
    }
}

// Document CRUD APIs
export const getAllDocuments = async (skip = 0, limit = 50, tags = null) => {
  try {
    const params = { skip, limit };
    if (tags) params.tags = tags;
    
    const response = await api.get('/documents/', { params });
    return response.data;
  } catch (error) {
    console.error('Get documents error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch documents');
  }
};

export const getDocument = async (documentId) => {
  try {
    const response = await api.get(`/documents/${documentId}`);
    return response.data;
  } catch (error) {
    console.error('Get document error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch document');
  }
};

export const createDocument = async (documentData) => {
  try {
    const response = await api.post('/documents/', documentData);
    return response.data;
  } catch (error) {
    console.error('Create document error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to create document');
  }
};

export const uploadDocument = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/documents/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Upload document error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to upload document');
  }
};

export const updateDocument = async (documentId, updateData) => {
  try {
    const response = await api.put(`/documents/${documentId}`, updateData);
    return response.data;
  } catch (error) {
    console.error('Update document error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to update document');
  }
};

export const deleteDocument = async (documentId) => {
  try {
    await api.delete(`/documents/${documentId}`);
    return true;
  } catch (error) {
    console.error('Delete document error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to delete document');
  }
};

export default api;
