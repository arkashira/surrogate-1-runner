import React, { useState, useEffect } from 'react';
import Task from './Task';
import axios from 'axios';

const TaskList = ({ userId }) => {
  const [tasks, setTasks] = useState([]);
  const [filterStatus, setFilterStatus] = useState('all');
  const [sortBy, setSortBy] = useState('priority');

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get(`/api/tasks?userId=${userId}`);
        setTasks(response.data);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };
    fetchTasks();
  }, [userId]);

  const handleStatusChange = (event) => {
    setFilterStatus(event.target.value);
  };

  const handleSortChange = (event) => {
    setSortBy(event.target.value);
  };

  const filteredTasks = tasks.filter(task => 
    filterStatus === 'all' || task.status === filterStatus
  );

  const sortedTasks = [...filteredTasks].sort((a, b) => {
    if (sortBy === 'priority') {
      return b.priority - a.priority;
    } else if (sortBy === 'dueDate') {
      return new Date(a.dueDate) - new Date(b.dueDate);
    }
    return 0;
  });

  const handleTaskUpdate = (taskId, newStatus) => {
    const updatedTasks = tasks.map(task => 
      task.id === taskId ? { ...task, status: newStatus } : task
    );
    setTasks(updatedTasks);

    axios.put(`/api/tasks/${taskId}`, { status: newStatus })
      .catch(error => console.error("Error updating task:", error));
  };

  return (
    <div>
      <select value={filterStatus} onChange={handleStatusChange}>
        <option value="all">All</option>
        <option value="pending">Pending</option>
        <option value="in-progress">In Progress</option>
        <option value="done">Done</option>
      </select>
      <select value={sortBy} onChange={handleSortChange}>
        <option value="priority">Priority</option>
        <option value="dueDate">Due Date</option>
      </select>
      <ul>
        {sortedTasks.map(task => (
          <Task key={task.id} task={task} onUpdate={handleTaskUpdate} />
        ))}
      </ul>
    </div>
  );
};

export default TaskList;