import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { reportService } from '../services/reportService';
import api from '../services/api';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Card } from '../components/Card';

export const ReportFormPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(!!id);
  const [error, setError] = useState('');
  const [projects, setProjects] = useState([]);
  const [formData, setFormData] = useState({
    project_id: '',
    week_start_date: '',
    tasks_completed: '',
    tasks_planned: '',
    blockers: '',
    hours_worked: '',
    notes: '',
  });

  useEffect(() => {
    api.get('/projects/').then(res => setProjects(res.data));
    if (id) {
      reportService.getReport(id).then(res => {
        setFormData(res.data);
        setLoading(false);
      });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent, submit = false) => {
    e.preventDefault();
    try {
      if (id) await reportService.updateReport(id, formData);
      else await reportService.createReport(formData);
      
      if (submit && id) await reportService.submitReport(id);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save report');
    }
  };

  if (loading) return <div className="p-10"><LoadingSpinner /></div>;

  return (
    <div className="p-8">
      <Card className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-6 text-gray-900">{id ? 'Edit' : 'Create'} Report</h2>
        {error && <ErrorAlert message={error} />}
        <form onSubmit={(e) => handleSubmit(e)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Project</label>
            <select value={formData.project_id} onChange={(e) => setFormData({...formData, project_id: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none">
                <option value="">Select Project</option>
                {projects.map((p: any) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <Input label="Week Start Date" type="date" value={formData.week_start_date} onChange={(e) => setFormData({...formData, week_start_date: e.target.value})} />
          <Input label="Tasks Completed" value={formData.tasks_completed} onChange={(e) => setFormData({...formData, tasks_completed: e.target.value})} />
          <Input label="Tasks Planned" value={formData.tasks_planned} onChange={(e) => setFormData({...formData, tasks_planned: e.target.value})} />
          <Input label="Blockers" value={formData.blockers} onChange={(e) => setFormData({...formData, blockers: e.target.value})} />
          <Input label="Hours Worked" type="number" value={formData.hours_worked} onChange={(e) => setFormData({...formData, hours_worked: e.target.value})} />
          
          <div className="flex gap-4 pt-4">
            <Button type="submit" className="flex-1">Save Draft</Button>
            {id && <Button type="button" variant="primary" onClick={(e) => handleSubmit(e as any, true)} className="flex-1 bg-green-600 hover:bg-green-700">Submit Report</Button>}
            <Button type="button" variant="secondary" onClick={() => navigate('/')} className="flex-1">Cancel</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
