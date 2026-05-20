import React, { useState, useEffect } from 'react';
import { fetchAgentHealth, fetchWorkflowMetrics, fetchTags } from './api';

const Dashboard = () => {
  const [agentHealth, setAgentHealth] = useState([]);
  const [workflowMetrics, setWorkflowMetrics] = useState([]);
  const [tags, setTags] = useState([]);
  const [selectedTag, setSelectedTag] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthData, metricsData, tagsData] = await Promise.all([
          fetchAgentHealth(),
          fetchWorkflowMetrics(),
          fetchTags()
        ]);
        setAgentHealth(healthData);
        setWorkflowMetrics(metricsData);
        setTags(tagsData);
      } catch (error) {
        console.error('Dashboard data fetch error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 1000); // <1s refresh rate

    return () => clearInterval(interval);
  }, []);

  const filteredMetrics = selectedTag 
    ? workflowMetrics.filter(metric => metric.tags.includes(selectedTag))
    : workflowMetrics;

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Surrogate-1 Live Dashboard</h1>
        <div className="tag-filter">
          <label htmlFor="tag-select">Filter by Tag:</label>
          <select 
            id="tag-select" 
            value={selectedTag} 
            onChange={(e) => setSelectedTag(e.target.value)}
          >
            <option value="">All Tags</option>
            {tags.map(tag => (
              <option key={tag} value={tag}>{tag}</option>
            ))}
          </select>
        </div>
      </header>

      <section className="agent-health">
        <h2>Agent Health Status</h2>
        {loading ? (
          <div className="loading">Loading agent data...</div>
        ) : (
          <div className="agent-grid">
            {agentHealth.map(agent => (
              <div key={agent.id} className={`agent-card ${agent.status}`}>
                <h3>{agent.name}</h3>
                <p>Status: {agent.status}</p>
                <p>CPU: {agent.cpu}%</p>
                <p>Memory: {agent.memory}%</p>
                <p>Last Update: {new Date(agent.lastUpdate).toLocaleTimeString()}</p>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="workflow-metrics">
        <h2>Workflow Execution Metrics</h2>
        {loading ? (
          <div className="loading">Loading workflow data...</div>
        ) : (
          <div className="workflow-grid">
            {filteredMetrics.map(workflow => (
              <div key={workflow.id} className="workflow-card">
                <h3>{workflow.name}</h3>
                <div className="latency-heatmap">
                  {Array.from({ length: 24 }).map((_, hour) => (
                    <div 
                      key={hour} 
                      className="heatmap-cell"
                      style={{ 
                        backgroundColor: `rgba(0, 0, 255, ${workflow.latency[hour] / 100})` 
                      }}
                    >
                      {workflow.latency[hour]}ms
                    </div>
                  ))}
                </div>
                <p>Avg Latency: {workflow.avgLatency}ms</p>
                <p>Success Rate: {workflow.successRate}%</p>
              </div>
            ))}
          </div>
        )}
      </section>

      <style jsx>{`
        .dashboard {
          padding: 20px;
          font-family: sans-serif;
          background-color: #f5f7fa;
          min-height: 100vh;
        }
        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 30px;
          padding: 15px;
          background: white;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .tag-filter select {
          padding: 8px;
          border-radius: 4px;
          border: 1px solid #ddd;
        }
        .agent-grid, .workflow-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 20px;
          margin-top: 20px;
        }
        .agent-card, .workflow-card {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .agent-card.healthy {
          border-left: 4px solid #4caf50;
        }
        .agent-card.warning {
          border-left: 4px solid #ff9800;
        }
        .agent-card.error {
          border-left: 4px solid #f44336;
        }
        .latency-heatmap {
          display: grid;
          grid-template-columns: repeat(24, 1fr);
          gap: 2px;
          margin: 10px 0;
        }
        .heatmap-cell {
          padding: 5px;
          text-align: center;
          font-size: 12px;
          border-radius: 3px;
        }
        .loading {
          text-align: center;
          padding: 40px;
          font-size: 18px;
          color: #666;
        }
      `}</style>
    </div>
  );
};

export default Dashboard;