import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export const Sidebar = () => {
  const { user } = useContext(AuthContext);
  
  return (
    <aside className="w-64 bg-gray-800 text-white h-screen">
      <div className="p-4 text-xl font-bold">App Sidebar</div>
      <nav className="p-4 space-y-2">
        <Link to="/" className="block p-2 hover:bg-gray-700">Reports</Link>
        {user?.role === 'manager' && (
          <Link to="/dashboard" className="block p-2 hover:bg-gray-700">Dashboard</Link>
        )}
        <Link to="/projects" className="block p-2 hover:bg-gray-700">Projects</Link>
      </nav>
    </aside>
  );
};
