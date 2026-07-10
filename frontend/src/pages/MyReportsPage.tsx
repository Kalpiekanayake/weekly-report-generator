import { useState, useEffect } from 'react';
import { reportService } from '../services/reportService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { Button } from '../components/Button';
import { Link } from 'react-router-dom';

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

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <div className="flex justify-between mb-4">
        <h2 className="text-2xl font-bold">My Reports</h2>
        <Button as={Link} to="/reports/new">Create Report</Button>
      </div>
      {error && <ErrorAlert message={error} />}
      <table className="min-w-full bg-white shadow rounded">
        <thead>
          <tr>
            <th className="p-4 border-b">Week</th>
            <th className="p-4 border-b">Project</th>
            <th className="p-4 border-b">Status</th>
            <th className="p-4 border-b">Submitted</th>
            <th className="p-4 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((r: any) => (
            <tr key={r.id}>
              <td className="p-4 border-b">{r.week_start_date}</td>
              <td className="p-4 border-b">{r.project_name}</td>
              <td className="p-4 border-b">{r.status}</td>
              <td className="p-4 border-b">{r.submitted_at || '-'}</td>
              <td className="p-4 border-b">
                <Link to={`/reports/${r.id}/edit`} className="text-blue-600">Edit</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
