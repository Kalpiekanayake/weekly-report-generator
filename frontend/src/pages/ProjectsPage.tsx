import { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { AuthContext } from '../context/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Button } from '../components/Button';

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

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <div className="flex justify-between mb-4">
        <h2 className="text-2xl font-bold">Projects</h2>
        {user?.role === 'manager' && (
          <Button as={Link} to="/projects/new" className="w-auto">Create Project</Button>
        )}
      </div>
      {error && <ErrorAlert message={error} />}
      <table className="min-w-full bg-white shadow rounded">
        <thead>
          <tr>
            <th className="p-4 border-b">Name</th>
            <th className="p-4 border-b">Description</th>
            {user?.role === 'manager' && <th className="p-4 border-b">Actions</th>}
          </tr>
        </thead>
        <tbody>
          {projects.map((p: any) => (
            <tr key={p.id}>
              <td className="p-4 border-b">{p.name}</td>
              <td className="p-4 border-b">{p.description}</td>
              {user?.role === 'manager' && (
                <td className="p-4 border-b space-x-2">
                  <Link to={`/projects/${p.id}/edit`} className="text-blue-600">Edit</Link>
                  <button onClick={() => handleDelete(p.id)} className="text-red-600">Delete</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
