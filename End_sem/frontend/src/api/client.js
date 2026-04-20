import axios from 'axios';

// Build API URL from environment or default
let API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Ensure /api is included in the URL
if (API_URL && !API_URL.endsWith('/api')) {
  API_URL = `${API_URL}/api`.replace(/\/api\/api$/, '/api'); // Prevent double /api
}

console.log('[API Client] Using base URL:', API_URL);

// Standard client with 30 second timeout
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Batch client with 3 minute timeout (batch operations can be slow)
const batchClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 180000,
});

export const predictSingle = async (data) => {
  const response = await apiClient.post('/predict', data);
  return response.data;
};

export const processBatch = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await batchClient.post('/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const runAgentPlanner = async () => {
  const response = await apiClient.post('/agent/run');
  return response.data;
};

export const getSampleData = async () => {
  const response = await apiClient.get('/data/sample');
  return response.data;
};

export const checkHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

export const checkUploadStatus = async () => {
  const response = await apiClient.get('/upload/status');
  return response.data;
};

export default apiClient;
