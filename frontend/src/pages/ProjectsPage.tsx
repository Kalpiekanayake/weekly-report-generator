import { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { AuthContext } from '../context/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Plus, Edit2, Trash2 } from 'lucide-react';

export const ProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useContext(AuthContext);

  const fetchProjects = () => {
    projectService.getAll()
      .then(res => setProjects(res.data))
      .catch(() => setError('Failed to load projects'))
      .finally(() => setLoading(false));
  };

  useEffect(fetchProjects, []);

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await projectService.delete(id);
        fetchProjects();
      } catch {
        setError('Failed to delete project');
      }
    }
  };

  if (loading) return <div className="p-10"><LoadingSpinner /></div>;

  return (
    <div className="space-y-6 p-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-900">Projects</h2>
        {user?.role === 'manager' && (
          <Button as={Link} to="/projects/new" className="flex items-center gap-2"><Plus className="w-4 h-4" /> Create Project</Button>
        )}
      </div>
      {error && <ErrorAlert message={error} />}
      
      <Card className="p-0 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b border-gray-100 text-gray-500">
            <tr>
              <th className="p-4">Name</th>
              <th className="p-4">Description</th>
              {user?.role === 'manager' && <th className="p-4 text-right">Actions</th>}
            </tr>
          </thead>
          <tbody>
            {projects.map((p: any) => (
              <tr key={p.id} className="border-b border-gray-50 hover:bg-gray-50">
                <td className="p-4 font-semibold text-gray-900">{p.name}</td>
                <td className="p-4 text-gray-600">{p.description}</td>
                {user?.role === 'manager' && (
                  <td className="p-4 text-right space-x-3">
                    <Link to={`/projects/${p.id}/edit`} className="text-indigo-600 hover:text-indigo-900"><Edit2 className="w-4 h-4" /></Link>
                    <button onClick={() => handleDelete(p.id)} className="text-red-600 hover:text-red-900"><Trash2 className="w-4 h-4" /></button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
};
