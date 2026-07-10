import { Navigate, Outlet } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { LoadingSpinner } from './LoadingSpinner';

export const ProtectedRoute = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <LoadingSpinner />;
  return user ? <Outlet /> : <Navigate to="/login" replace />;
};

export const ManagerRoute = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <LoadingSpinner />;
  return user?.role === 'manager' ? <Outlet /> : <Navigate to="/" replace />;
};

export const PublicRoute = () => {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <LoadingSpinner />;
  return user ? <Navigate to="/" replace /> : <Outlet />;
};
