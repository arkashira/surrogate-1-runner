import React, { useState, useEffect } from 'react';
import { configureNotification } from '../services/notificationService';

const NotificationConfig = () => {
  const [slackWebhook, setSlackWebhook] = useState('');
  const [emailTemplate, setEmailTemplate] = useState('default');
  const [enableAssigned, setEnableAssigned] = useState(false);
  const [enableStatusChange, setEnableStatusChange] = useState(false);
  const [status, setStatus] = useState('');

  useEffect(() => {
    // Load existing config from localStorage (or any persistence layer)
    const stored = localStorage.getItem('notificationConfig');
    if (stored) {
      const cfg = JSON.parse(stored);
      setSlackWebhook(cfg.slackWebhook || '');
      setEmailTemplate(cfg.emailTemplate || 'default');
      setEnableAssigned(cfg.enableAssigned || false);
      setEnableStatusChange(cfg.enableStatusChange || false);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const config = {
      slackWebhook,
      emailTemplate,
      enableAssigned,
      enableStatusChange,
    };
    try {
      await configureNotification(config);
      setStatus('Configuration saved successfully.');
    } catch (err) {
      setStatus(`Error: ${err.message}`);
    }
  };

  return (
    <div className="notification-config">
      <h2>Notification Configuration</h2>
      {status && <p>{status}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Slack Webhook URL:
            <input
              type="url"
              value={slackWebhook}
              onChange={(e) => setSlackWebhook(e.target.value)}
              placeholder="https://hooks.slack.com/services/..."
            />
          </label>
        </div>
        <div>
          <label>
            Email Template:
            <select
              value={emailTemplate}
              onChange={(e) => setEmailTemplate(e.target.value)}
            >
              <option value="default">Default</option>
              <option value="detailed">Detailed</option>
              <option value="brief">Brief</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              checked={enableAssigned}
              onChange={(e) => setEnableAssigned(e.target.checked)}
            />
            Notify on Task Assigned
          </label>
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              checked={enableStatusChange}
              onChange={(e) => setEnableStatusChange(e.target.checked)}
            />
            Notify on Status Change
          </label>
        </div>
        <button type="submit">Save Configuration</button>
      </form>
    </div>
  );
};

export default NotificationConfig;