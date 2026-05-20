import React, { useState, useEffect } from 'react';
import './Notifications.css';

/**
 * Notification component
 *
 * Props:
 * - notifications: Array of { id, type, message }
 * - onClose: function(id) called when a notification is dismissed
 * - settings: { enabled: boolean, autoDismiss: boolean, dismissTimeout: number }
 * - onSettingsChange: function(updatedSettings)
 *
 * The component displays a list of notifications and a simple settings panel.
 */
const Notifications = ({
  notifications = [],
  onClose = () => {},
  settings = { enabled: true, autoDismiss: false, dismissTimeout: 5000 },
  onSettingsChange = () => {},
}) => {
  const [currentNotifs, setCurrentNotifs] = useState(notifications);

  useEffect(() => {
    setCurrentNotifs(notifications);
  }, [notifications]);

  // Auto-dismiss logic
  useEffect(() => {
    if (!settings.autoDismiss) return;
    const timers = currentNotifs.map((n) =>
      setTimeout(() => onClose(n.id), settings.dismissTimeout)
    );
    return () => timers.forEach(clearTimeout);
  }, [currentNotifs, settings.autoDismiss, settings.dismissTimeout, onClose]);

  const toggleEnabled = () => {
    onSettingsChange({ ...settings, enabled: !settings.enabled });
  };

  const toggleAutoDismiss = () => {
    onSettingsChange({ ...settings, autoDismiss: !settings.autoDismiss });
  };

  if (!settings.enabled) return null;

  return (
    <div className="notifications-wrapper">
      <div className="notifications-settings">
        <label>
          <input
            type="checkbox"
            checked={settings.autoDismiss}
            onChange={toggleAutoDismiss}
          />{' '}
          Auto‑dismiss
        </label>
        <button onClick={toggleEnabled} className="settings-btn">
          {settings.enabled ? 'Disable' : 'Enable'} Notifications
        </button>
      </div>
      <div className="notifications-container">
        {currentNotifs.map((n) => (
          <div key={n.id} className={`notification ${n.type}`}>
            <span>{n.message}</span>
            <button
              className="close-btn"
              onClick={() => onClose(n.id)}
              aria-label="Dismiss notification"
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Notifications;