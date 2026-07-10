import { useState, useEffect } from 'react';
import { reportService } from '../services/reportService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Button } from '../components/Button';
import { Link } from 'react-router-dom';
import { Card } from '../components/Card';
import { Plus } from 'lucide-react';

export const MyReportsPage = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    reportService.getMyReports()
      .then(res => setReports(res.data))
      .catch(() => setError('Failed to load reports'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-10"><LoadingSpinner /></div>;

  return (
    <div className="space-y-6 p-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-900">My Weekly Reports</h2>
        <Button as={Link} to="/reports/new" className="flex items-center gap-2"><Plus className="w-4 h-4" /> Create Report</Button>
      </div>
      
      {error && <ErrorAlert message={error} />}
      
      <Card className="p-0 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b border-gray-100 text-gray-500">
            <tr>
              <th className="p-4">Week</th>
              <th className="p-4">Project</th>
              <th className="p-4">Status</th>
              <th className="p-4">Submitted</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((r: any) => (
              <tr key={r.id} className="border-b border-gray-50 hover:bg-gray-50">
                <td className="p-4 font-medium">{r.week_start_date}</td>
                <td className="p-4">{r.project_name}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${r.status === 'submitted' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
                    {r.status}
                  </span>
                </td>
                <td className="p-4 text-gray-600">{r.submitted_at ? new Date(r.submitted_at).toLocaleDateString() : '-'}</td>
                <td className="p-4 text-right">
                  <Link to={`/reports/${r.id}/edit`} className="text-indigo-600 hover:text-indigo-900 font-medium">Edit</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
};
