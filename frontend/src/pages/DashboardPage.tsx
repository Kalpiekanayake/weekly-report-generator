import { useState, useEffect } from 'react';
import { dashboardService } from '../services/dashboardService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorAlert } from '../components/ErrorAlert';
import { LineChartComponent } from '../components/charts/LineChartComponent';
import { BarChartComponent } from '../components/charts/BarChartComponent';
import { PieChartComponent } from '../components/charts/PieChartComponent';

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

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error} />;

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
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Manager Dashboard</h2>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="bg-white p-4 rounded shadow">
            <div className="text-gray-500">{s.label}</div>
            <div className="text-2xl font-bold">{s.value}</div>
          </div>
        ))}
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-4">Reports per Week</h3>
          <LineChartComponent data={analytics.reports_per_week} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-4">Reports by Project</h3>
          <BarChartComponent data={analytics.reports_by_project} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-4">Reports by Team Member</h3>
          <BarChartComponent data={analytics.reports_by_member} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-4">Submission Status Distribution</h3>
          <PieChartComponent data={analytics.status_distribution} />
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-4">Open Blockers by Project</h3>
          <BarChartComponent data={analytics.open_blockers_by_project} />
        </div>
      </div>

      {/* Project Summary */}
      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-lg font-bold mb-4">Project Summary</h3>
        <table className="min-w-full">
          <thead>
            <tr>
              <th className="text-left p-2">Project</th>
              <th className="text-left p-2">Members</th>
              <th className="text-left p-2">Reports</th>
            </tr>
          </thead>
          <tbody>
            {data.project_summaries.map((p: any) => (
              <tr key={p.project_name}>
                <td className="p-2 border-t">{p.project_name}</td>
                <td className="p-2 border-t">{p.num_members}</td>
                <td className="p-2 border-t">{p.num_reports}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-lg font-bold mb-4">Recent Activity</h3>
        <ul className="space-y-2">
          {data.recent_activity.map((a: any) => (
            <li key={a.report_id} className="border-t pt-2">
              <span className="font-semibold">{a.user_name}</span> submitted report for {a.project_name} (Week: {a.week_start_date})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
