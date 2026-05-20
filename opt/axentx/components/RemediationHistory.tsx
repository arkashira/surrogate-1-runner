import React, { useEffect, useState } from 'react';
import { remediationLogService } from '../services/RemediationLogService';
import { RemediationAction } from '../types';

interface RemediationHistoryProps {
  anomalyId?: string;
  team?: string;
  status?: RemediationAction['status'];
}

const RemediationHistory: React.FC<RemediationHistoryProps> = ({
  anomalyId,
  team,
  status
}) => {
  const [remediationHistory, setRemediationHistory] = useState<RemediationAction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        let history: RemediationAction[] = [];

        if (anomalyId) {
          history = remediationLogService.getRemediationHistoryByAnomaly(anomalyId);
        } else if (team) {
          history = remediationLogService.getRemediationHistoryByTeam(team);
        } else if (status) {
          history = remediationLogService.getRemediationHistoryByStatus(status);
        } else {
          history = remediationLogService.getRemediationHistory();
        }

        setRemediationHistory(history);
      } catch (err) {
        setError('Failed to load remediation history');
        console.error('Error loading remediation history:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [anomalyId, team, status]);

  if (loading) return <div>Loading remediation history...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="remediation-history">
      <h2>Remediation History</h2>
      {remediationHistory.length === 0 ? (
        <p>No remediation actions found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Action</th>
              <th>User</th>
              <th>Status</th>
              <th>Team</th>
            </tr>
          </thead>
          <tbody>
            {remediationHistory.map((action, index) => (
              <tr key={`${action.anomalyId}-${index}`}>
                <td>{new Date(action.timestamp).toLocaleString()}</td>
                <td>{action.action}</td>
                <td>{action.user}</td>
                <td>
                  <span className={`status-badge ${action.status}`}>
                    {action.status}
                  </span>
                </td>
                <td>{action.team}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default RemediationHistory;