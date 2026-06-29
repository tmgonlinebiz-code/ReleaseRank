import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fileService = {
  upload: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return apiClient.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  list: async () => {
    return apiClient.get('/files/list');
  },

  getInfo: async (fileId: string) => {
    return apiClient.get(`/files/info/${fileId}`);
  },

  delete: async (fileId: string) => {
    return apiClient.delete(`/files/delete/${fileId}`);
  },
};

export const healthService = {
  check: async () => {
    return apiClient.get('/health');
  },
};

export default apiClient;
