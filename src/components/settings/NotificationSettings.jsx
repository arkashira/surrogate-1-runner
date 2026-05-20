import React, { useState, useEffect } from 'react';
import { notificationService } from '../../services/notificationService';

const NotificationSettings = ({ projectId }) => {
  const [settings, setSettings] = useState({
    slackWebhook: '',
    email: '',
    threshold: 20,
  });

  useEffect(() => {
    const fetchSettings = async () => {
      const data = await notificationService.getNotificationSettings(projectId);
      setSettings(data);
    };
    fetchSettings();
  }, [projectId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await notificationService.updateNotificationSettings(projectId, settings);
    alert('Settings updated successfully');
  };

  return (
    <div className="notification-settings">
      <h2>Notification Settings</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Slack Webhook URL:</label>
          <input
            type="text"
            name="slackWebhook"
            value={settings.slackWebhook}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={settings.email}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Threshold (%):</label>
          <input
            type="number"
            name="threshold"
            value={settings.threshold}
            onChange={handleChange}
            min="1"
            max="100"
          />
        </div>
        <button type="submit">Save Settings</button>
      </form>
    </div>
  );
};

export default NotificationSettings;