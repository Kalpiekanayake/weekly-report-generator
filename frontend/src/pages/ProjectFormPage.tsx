import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Card } from '../components/Card';

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

  if (loading) return <div className="p-10"><LoadingSpinner /></div>;

  return (
    <div className="p-8">
      <Card className="max-w-xl mx-auto">
        <h2 className="text-2xl font-bold mb-6 text-gray-900">{id ? 'Edit' : 'Create'} Project</h2>
        {error && <ErrorAlert message={error} />}
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Project Name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} required />
          <Input label="Description" value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} />
          <div className="flex gap-4 pt-4">
            <Button type="submit" className="flex-1">Save Project</Button>
            <Button type="button" variant="secondary" onClick={() => navigate('/projects')} className="flex-1">Cancel</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
