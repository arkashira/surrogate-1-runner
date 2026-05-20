import React from 'react';
import { Task } from '../types';

interface TasksListProps {
  tasks: Task[];
}

const TasksList: React.FC<TasksListProps> = ({ tasks }) => {
  return (
    <div className="tasks-list">
      {tasks.map((task) => (
        <div key={task.id} className="task-item">
          <div className="task-status">
            <span className={`status-indicator ${task.status.toLowerCase()}`}></span>
            <span>{task.status}</span>
          </div>
          <div className="task-details">
            <span>{task.name}</span>
            <span>{task.dataSize}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TasksList;