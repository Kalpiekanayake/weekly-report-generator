import api from './api';

export const reportService = {
  getMyReports: () => api.get('/reports/my/'),
  getReport: (id: string) => api.get(`/reports/${id}/`),
  createReport: (data: any) => api.post('/reports/', data),
  updateReport: (id: string, data: any) => api.put(`/reports/${id}/`, data),
  submitReport: (id: string) => api.post(`/reports/${id}/submit/`),
};
