import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PipelineDetail = ({ match }) => {
  const [pipeline, setPipeline] = useState({});
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPipeline = async () => {
      try {
        const response = await axios.get(`/api/pipelines/${match.params.id}`);
        setPipeline(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    const fetchLogs = async () => {
      try {
        const response = await axios.get(`/api/pipelines/${match.params.id}/logs`);
        setLogs(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchPipeline();
    fetchLogs();
    setLoading(false);
  }, [match.params.id]);

  return (
    <div>
      <h1>Pipeline Detail</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <h2>{pipeline.name}</h2>
          <p>Last Run Time: {pipeline.lastRunTime}</p>
          <p>Status: {pipeline.status}</p>
          <h3>Recent Logs</h3>
          <ul>
            {logs.map((log) => (
              <li key={log.id}>{log.message}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default PipelineDetail;