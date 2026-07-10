import { Link } from 'react-router-dom';

export const Sidebar = () => (
  <aside className="w-64 bg-gray-800 text-white h-screen">
    <div className="p-4 text-xl font-bold">App Sidebar</div>
    <nav className="p-4 space-y-2">
      <Link to="/" className="block p-2 hover:bg-gray-700">Reports</Link>
      <Link to="/dashboard" className="block p-2 hover:bg-gray-700">Dashboard</Link>
      <Link to="/projects" className="block p-2 hover:bg-gray-700">Projects</Link>
    </nav>
  </aside>
);
