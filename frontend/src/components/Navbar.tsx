import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { UserCircle } from 'lucide-react';

export const Navbar = () => {
  const { user } = useContext(AuthContext);
  
  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
      <div className="font-semibold text-gray-700">Welcome, {user?.full_name}</div>
      <div className="flex items-center gap-2 text-gray-500">
        <UserCircle className="w-8 h-8" />
        <span className="text-sm font-medium">{user?.role}</span>
      </div>
    </nav>
  );
};
