import { useState, useEffect } from 'react';
import { dashboardService } from '../services/dashboardService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { LineChartComponent } from '../components/charts/LineChartComponent';
import { BarChartComponent } from '../components/charts/BarChartComponent';
import { PieChartComponent } from '../components/charts/PieChartComponent';
import { Card } from '../components/Card';
import { TeamReportsTable } from '../components/TeamReportsTable';

export const DashboardPage = () => {
  const [data, setData] = useState<any>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      dashboardService.getDashboardData(),
      dashboardService.getAnalyticsData()
    ])
      .then(([res1, res2]) => {
        setData(res1.data);
        setAnalytics(res2.data);
      })
      .catch(() => setError('Failed to load dashboard'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-10"><LoadingSpinner /></div>;
  if (error) return <div className="p-10"><ErrorAlert message={error} /></div>;

  const stats = [
    { label: 'Total Users', value: data.total_users },
    { label: 'Total Projects', value: data.total_projects },
    { label: 'Total Reports', value: data.total_reports },
    { label: 'Draft Reports', value: data.draft_reports },
    { label: 'Submitted Reports', value: data.submitted_reports },
    { label: 'Pending Reports', value: data.pending_reports },
    { label: 'Late Reports', value: data.late_reports },
  ];

  return (
    <div className="space-y-8 p-8">
      <h2 className="text-3xl font-bold text-gray-900">Manager Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {stats.map((s) => (
          <Card key={s.label}>
            <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">{s.label}</div>
            <div className="text-3xl font-bold text-indigo-900 mt-2">{s.value}</div>
          </Card>
        ))}
      </div>

      <TeamReportsTable />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card><h3 className="font-semibold text-lg mb-4">Reports per Week</h3><LineChartComponent data={analytics.reports_per_week} /></Card>
        <Card><h3 className="font-semibold text-lg mb-4">Reports by Project</h3><BarChartComponent data={analytics.reports_by_project} /></Card>
        <Card><h3 className="font-semibold text-lg mb-4">Reports by Team Member</h3><BarChartComponent data={analytics.reports_by_member} /></Card>
        <Card><h3 className="font-semibold text-lg mb-4">Submission Status</h3><PieChartComponent data={analytics.status_distribution} /></Card>
        <Card className="lg:col-span-2"><h3 className="font-semibold text-lg mb-4">Open Blockers by Project</h3><BarChartComponent data={analytics.open_blockers_by_project} /></Card>
      </div>

      <Card>
        <h3 className="text-xl font-bold mb-6">Project Summary</h3>
        <table className="w-full text-left">
          <thead className="border-b border-gray-100 text-gray-500">
            <tr><th className="p-4">Project</th><th className="p-4">Members</th><th className="p-4">Reports</th></tr>
          </thead>
          <tbody>
            {data.project_summaries.map((p: any) => (
              <tr key={p.project_name} className="hover:bg-gray-50">
                <td className="p-4 font-medium text-gray-900">{p.project_name}</td>
                <td className="p-4 text-gray-600">{p.num_members}</td>
                <td className="p-4 text-gray-600">{p.num_reports}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      <Card>
        <h3 className="text-xl font-bold mb-6">Recent Activity</h3>
        <ul className="space-y-4">
          {data.recent_activity.map((a: any) => (
            <li key={a.report_id} className="border-b border-gray-100 pb-4 last:border-0 last:pb-0">
              <p className="text-gray-800"><span className="font-semibold text-indigo-900">{a.user_name}</span> submitted report for <span className="font-medium">{a.project_name}</span></p>
              <p className="text-xs text-gray-400 mt-1">Week: {a.week_start_date} • {a.submitted_at}</p>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
};
