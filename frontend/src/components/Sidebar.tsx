import { LayoutDashboard, FileText, FolderKanban, LogOut, Bot } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export const Sidebar = () => {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();

  const navItems = [
    { to: '/', label: 'Reports', icon: FileText },
    { to: '/projects', label: 'Projects', icon: FolderKanban },
    ...(user?.role === 'manager' ? [
      { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
      { to: '/ai', label: 'AI Assistant', icon: Bot }
    ] : []),
  ];

  return (
    <aside className="w-64 bg-indigo-900 text-indigo-50 h-screen flex flex-col shadow-xl">
      <div className="p-6 text-xl font-bold flex items-center gap-2 text-white">
        <LayoutDashboard className="w-8 h-8 text-indigo-400" />
        SaaS Report
      </div>
      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => {
          const isActive = location.pathname === item.to;
          return (
            <Link 
              key={item.to} 
              to={item.to} 
              className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-indigo-800 text-white' : 'hover:bg-indigo-800'}`}
            >
              <item.icon className="w-5 h-5" />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-indigo-800">
        <button onClick={logout} className="flex items-center gap-3 w-full p-3 text-indigo-300 hover:text-white transition-colors">
          <LogOut className="w-5 h-5" />
          Logout
        </button>
      </div>
    </aside>
  );
};
