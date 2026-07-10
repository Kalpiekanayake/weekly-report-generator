import { Navigate, Outlet } from 'react-router-dom';

export const ProtectedRoute = () => {
  // Replace with actual auth logic
  const isAuthenticated = false; 

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};
