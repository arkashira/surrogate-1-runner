import React from 'react';
import { WorkflowProvider } from './contexts/WorkflowContext';
import WorkflowDashboard from './components/WorkflowDashboard';
import './App.css';

const App: React.FC = () => {
  return (
    <WorkflowProvider>
      <div className="App">
        <header className="App-header">
          <h1>Workflow Monitoring Dashboard</h1>
        </header>
        <main>
          <WorkflowDashboard />
        </main>
      </div>
    </WorkflowProvider>
  );
};

export default App;