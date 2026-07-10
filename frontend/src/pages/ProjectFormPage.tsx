import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';

export const ProjectFormPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({ name: '', description: '' });

  useEffect(() => {
    if (id) {
      projectService.getById(id).then(res => {
        setFormData(res.data);
        setLoading(false);
      });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (id) await projectService.update(id, formData);
      else await projectService.create(formData);
      navigate('/projects');
    } catch {
      setError('Failed to save project');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-6">{id ? 'Edit' : 'Create'} Project</h2>
      {error && <ErrorAlert message={error} />}
      <form onSubmit={handleSubmit}>
        <Input label="Name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} required />
        <Input label="Description" value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} />
        <Button type="submit">Save</Button>
      </form>
    </div>
  );
};
