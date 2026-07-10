import { useState, useEffect } from 'react';
import { reportService } from '../services/reportService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Card } from '../components/Card';
import { Input } from '../components/Input';
import api from '../services/api';

export const TeamReportsTable = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    user_id: '',
    project_id: '',
    week_start_date: '',
    status: ''
  });
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.get('/projects/').then(res => setProjects(res.data));
    fetchReports();
  }, [filters]);

  const fetchReports = () => {
    setLoading(true);
    // Build query params
    const params = new URLSearchParams(filters).toString();
    api.get(`/reports/?${params}`)
      .then(res => setReports(res.data))
      .catch(() => setError('Failed to load team reports'))
      .finally(() => setLoading(false));
  };

  if (loading && reports.length === 0) return <LoadingSpinner />;

  return (
    <Card className="mt-8">
      <h3 className="text-xl font-bold mb-6">Team Reports</h3>
      
      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Input label="Team Member ID" value={filters.user_id} onChange={(e) => setFilters({...filters, user_id: e.target.value})} />
        <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Project</label>
            <select value={filters.project_id} onChange={(e) => setFilters({...filters, project_id: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2">
                <option value="">All Projects</option>
                {projects.map((p: any) => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
        </div>
        <Input label="Week Start" type="date" value={filters.week_start_date} onChange={(e) => setFilters({...filters, week_start_date: e.target.value})} />
        <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select value={filters.status} onChange={(e) => setFilters({...filters, status: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2">
                <option value="">All Statuses</option>
                <option value="draft">Draft</option>
                <option value="submitted">Submitted</option>
            </select>
        </div>
      </div>

      {error && <ErrorAlert message={error} />}
      
      <table className="w-full text-left">
        <thead className="bg-gray-50 border-b border-gray-100 text-gray-500">
          <tr>
            <th className="p-4">Member</th>
            <th className="p-4">Week</th>
            <th className="p-4">Project</th>
            <th className="p-4">Status</th>
            <th className="p-4">Submitted</th>
          </tr>
        </thead>
        <tbody>
          {reports.length === 0 ? <tr><td colSpan={5} className="p-4 text-center">No reports found</td></tr> : 
          reports.map((r: any) => (
            <tr key={r.id} className="border-b border-gray-50 hover:bg-gray-50">
              <td className="p-4 font-medium">{r.user_full_name}</td>
              <td className="p-4">{r.week_start_date}</td>
              <td className="p-4">{r.project_name}</td>
              <td className="p-4">
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${r.status === 'submitted' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
                  {r.status}
                </span>
              </td>
              <td className="p-4">{r.submitted_at ? new Date(r.submitted_at).toLocaleDateString() : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
};
