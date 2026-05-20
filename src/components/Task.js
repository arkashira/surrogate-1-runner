
import React, { useState, useEffect } from 'react';
import styles from './Task.css';

const Task = ({ task }) => {
  const [isCompleted, setIsCompleted] = useState(task.isCompleted);

  useEffect(() => {
    setIsCompleted(task.isCompleted);
  }, [task.isCompleted]);

  return (
    <div className={styles.task}>
      <div className={styles.taskTitle}>{task.title}</div>
      <div className={styles.taskDescription}>{task.description}</div>
      <div className={styles.taskStatus}>
        {isCompleted ? (
          <div className={styles.completed}>Completed</div>
        ) : (
          <div className={styles.incomplete}>Incomplete</div>
        )}
      </div>
    </div>
  );
};

export default Task;

// src/styles/Task.css

.task {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.taskTitle {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.taskDescription {
  font-size: 16px;
  margin-bottom: 10px;
}

.taskStatus {
  display: flex;
  justify-content: center;
}

.completed {
  background-color: #4caf50;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.incomplete {
  background-color: #f44336;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}