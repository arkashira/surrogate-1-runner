import React from 'react';
import { Anomaly } from '../types/anomaly';

interface AnomalyCardProps {
  anomaly: Anomaly;
}

const AnomalyCard: React.FC<AnomalyCardProps> = ({ anomaly }) => {
  return (
    <div>
      <h2>{anomaly.name}</h2>
      <p>Severity: {anomaly.severity}</p>
      <p>Type: {anomaly.type}</p>
      <p>Time Range: {anomaly.startTime} - {anomaly.endTime}</p>
    </div>
  );
};

export default AnomalyCard;