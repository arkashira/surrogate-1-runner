import axios from 'axios';

const API_BASE_URL = 'https://api.surrogate-1.com';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Interceptor to add Auth Token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken'); // Retrieve token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const getRepositories = async (userId: number) => {
  // Note: In a real app, the backend usually gets the user from the token, 
  // so we might not need to pass userId in the URL, but keeping for context.
  const response = await apiClient.get(`/users/${userId}/repositories`);
  return response.data;
};

export const connectRepository = async (userId: number, repoUrl: string) => {
  const response = await apiClient.post(`/users/${userId}/repositories`, { repoUrl });
  return response.data;
};

export const deleteRepository = async (repoId: number) => {
  const response = await apiClient.delete(`/repositories/${repoId}`);
  return response.data;
};