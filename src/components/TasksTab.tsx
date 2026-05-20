import React from 'react';
import TasksList from './TasksList';
import { Task } from '../types';

const TasksTab: React.FC = () => {
  const tasks: Task[] = [
    { id: '1', name: 'Task 1', status: 'Running', dataSize: '100 MB' },
    { id: '2', name: 'Task 2', status: 'Completed', dataSize: '200 MB' },
    // Add more tasks as needed
  ];

  return (
    <div className="tasks-tab">
      <h2>Tasks</h2>
      <TasksList tasks={tasks} />
    </div>
  );
};

export default TasksTab;