import api from './api';

export const dashboardService = {
  getDashboardData: () => api.get('/dashboard/'),
  getAnalyticsData: () => api.get('/dashboard/analytics/'),
};
