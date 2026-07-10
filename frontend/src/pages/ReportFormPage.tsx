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
  const [report, setReport] = useState<any>(null);
  const [formData, setFormData] = useState({
    project_id: '',
    week_start_date: '',
    tasks_completed: '',
    tasks_planned: '',
    blockers: '',
    hours_worked: '',
    notes: '',
  });

  const isSubmitted = report?.status === 'submitted';

  useEffect(() => {
    api.get('/projects/').then(res => setProjects(res.data));
    if (id) {
      reportService.getReport(id).then(res => {
        setReport(res.data);
        setFormData(res.data);
        setLoading(false);
      });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent, submit = false) => {
    e.preventDefault();
    if (!formData.project_id || !formData.week_start_date || !formData.tasks_completed || !formData.tasks_planned || !formData.blockers) {
        setError('Please fill in all required fields.');
        return;
    }
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
        <h2 className="text-2xl font-bold mb-6 text-gray-900">{id ? (isSubmitted ? 'View' : 'Edit') : 'Create'} Report</h2>
        {error && <ErrorAlert message={error} />}
        <form onSubmit={(e) => handleSubmit(e)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Project</label>
            <select disabled={isSubmitted} value={formData.project_id} onChange={(e) => setFormData({...formData, project_id: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 outline-none disabled:bg-gray-100">
                <option value="">Select Project</option>
                {projects.map((p: any) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <Input disabled={isSubmitted} label="Week Start Date" type="date" value={formData.week_start_date} onChange={(e) => setFormData({...formData, week_start_date: e.target.value})} required />
          <Input disabled={isSubmitted} label="Tasks Completed" value={formData.tasks_completed} onChange={(e) => setFormData({...formData, tasks_completed: e.target.value})} required />
          <Input disabled={isSubmitted} label="Tasks Planned" value={formData.tasks_planned} onChange={(e) => setFormData({...formData, tasks_planned: e.target.value})} required />
          <Input disabled={isSubmitted} label="Blockers" value={formData.blockers} onChange={(e) => setFormData({...formData, blockers: e.target.value})} required />
          <Input disabled={isSubmitted} label="Hours Worked" type="number" value={formData.hours_worked} onChange={(e) => setFormData({...formData, hours_worked: e.target.value})} />
          <Input disabled={isSubmitted} label="Notes" value={formData.notes} onChange={(e) => setFormData({...formData, notes: e.target.value})} />
          
          {!isSubmitted && (
            <div className="flex gap-4 pt-4">
              <Button type="submit" className="flex-1">Save Draft</Button>
              {id && <Button type="button" variant="primary" onClick={(e) => handleSubmit(e as any, true)} className="flex-1 bg-green-600 hover:bg-green-700">Submit Report</Button>}
              <Button type="button" variant="secondary" onClick={() => navigate('/')} className="flex-1">Cancel</Button>
            </div>
          )}
        </form>
      </Card>
    </div>
  );
};
