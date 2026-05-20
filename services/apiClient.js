const fetch = require('node-fetch');

const apiClient = {
  async getTaskStatuses() {
    try {
      const response = await fetch('http://localhost:3000/api/tasks');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.map(task => ({
        id: task.id,
        status: task.status, // 'running' | 'completed'
        createdAt: task.created_at,
        totalDataSize: task.total_data_size || 0
      }));
    } catch (error) {
      console.error('Failed to fetch task statuses:', error);
      return [];
    }
  }
};

module.exports = apiClient;