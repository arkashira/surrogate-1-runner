const API_BASE = '/api/notifications';

const notificationService = {
  async getNotificationSettings(projectId) {
    const response = await fetch(`${API_BASE}/${projectId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch notification settings');
    }
    return response.json();
  },

  async updateNotificationSettings(projectId, settings) {
    const response = await fetch(`${API_BASE}/${projectId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(settings),
    });
    if (!response.ok) {
      throw new Error('Failed to update notification settings');
    }
  },
};

export { notificationService };