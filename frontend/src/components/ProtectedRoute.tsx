import { Navigate, Outlet } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { LoadingSpinner } from './LoadingSpinner';

export const ProtectedRoute = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <LoadingSpinner />;
  return user ? <Outlet /> : <Navigate to="/login" replace />;
};
