import React from 'react';
import TasksTab from './TasksTab';

const InstancePage: React.FC = () => {
  return (
    <div className="instance-page">
      <h1>Instance Page</h1>
      <TasksTab />
    </div>
  );
};

export default InstancePage;