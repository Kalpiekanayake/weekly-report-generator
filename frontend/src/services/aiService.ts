import api from './api';

export const aiService = {
  chat: (data: any) => api.post('/ai/chat', data),
  getHistory: () => api.get('/ai/history'),
};
