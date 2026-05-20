import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance with auth header
const api = axios.create({
  baseURL: `${API_BASE_URL}/projects`,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});

// CRUD operations
export const getProjects = () => api.get('/');
export const createProject = (projectData) => api.post('/', projectData);
export const deleteProject = (projectId) => api.delete(`/${projectId}`);
export const cancelIngestion = (projectId) => api.post(`/${projectId}/cancel`);

// Error handling interceptor
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);