import React from 'react';
import { Button, StatusIndicator } from '@axentx/ui-components';

const TaskItem = ({ task, updateTaskStatus }) => {
  const handleStatusUpdate = (newStatus) => {
    updateTaskStatus(task.id, newStatus);
  };

  return (
    <div>
      <h2>{task.title}</h2>
      <p>{task.description}</p>
      <StatusIndicator status={task.status} />
      {task.status === 'pending' && (
        <Button onClick={() => handleStatusUpdate('in-progress')}>Start</Button>
      )}
      {task.status === 'in-progress' && (
        <Button onClick={() => handleStatusUpdate('done')}>Finish</Button>
      )}
    </div>
  );
};

export default TaskItem;