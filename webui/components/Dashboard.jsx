import React, { useEffect, useState } from 'react';
import './dashboard.css';

const Dashboard = () => {
  const [labsData, setLabsData] = useState([]);
  const [errorTracking, setErrorTracking] = useState([]);
  const [examReadinessScore, setExamReadinessScore] = useState(0);

  useEffect(() => {
    // Fetch data from backend API
    fetch('/api/labs-performance')
      .then(response => response.json())
      .then(data => {
        setLabsData(data.labs);
        setErrorTracking(data.errors);
        setExamReadinessScore(data.examReadinessScore);
      });
  }, []);

  return (
    <div className="dashboard">
      <h1>Performance Dashboard</h1>
      <div className="completion-times">
        <h2>Completion Time Per Lab</h2>
        <ul>
          {labsData.map(lab => (
            <li key={lab.id}>
              {lab.name}: {lab.completionTime} seconds
            </li>
          ))}
        </ul>
      </div>
      <div className="error-tracking">
        <h2>Error Tracking</h2>
        <ul>
          {errorTracking.map(error => (
            <li key={error.id}>
              {error.message} - Root Cause: {error.rootCause}
            </li>
          ))}
        </ul>
      </div>
      <div className="exam-readiness">
        <h2>Exam Readiness Score</h2>
        <p>{examReadinessScore}/100</p>
      </div>
    </div>
  );
};

export default Dashboard;