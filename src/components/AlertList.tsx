import React from 'react';
import { Link } from 'react-router-dom';

interface Alert {
  id: string;
  message: string;
}

interface AlertListProps {
  alerts: Alert[];
}

const AlertList: React.FC<AlertListProps> = ({ alerts }) => {
  return (
    <div className="alert-list">
      <h2>Alerts</h2>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id}>
            <Link to={`/alerts/${alert.id}/root-cause`}>{alert.message}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AlertList;