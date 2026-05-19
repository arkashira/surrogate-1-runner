import React from 'react';

const Task = ({ task, onUpdate }) => {
  const handleStatusChange = (newStatus) => {
    onUpdate(task.id, newStatus);
  };

  return (
    <li>
      <strong>{task.title}</strong>
      <p>{task.description}</p>
      <p>Status: {task.status}</p>
      <button onClick={() => handleStatusChange('in-progress')}>Mark In Progress</button>
      <button onClick={() => handleStatusChange('done')}>Mark Done</button>
    </li>
  );
};

export default Task;