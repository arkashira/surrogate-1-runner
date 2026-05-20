import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './NotificationSystem.css';

/**
 * A lightweight, dismissible notification system.
 *
 * Props
 * -----
 * initialNotifications: Array of notification objects:
 *   {
 *     id: string (unique),
 *     title: string,
 *     body: string
 *   }
 *
 * The component maintains its own internal list and removes a notification
 * when the user clicks the dismiss button. It does not block UI interaction
 * and uses `aria-live="polite"` for accessibility.
 */
export function NotificationSystem({ initialNotifications = [] }) {
  const [notifications, setNotifications] = useState(initialNotifications);

  const dismiss = (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <div className="notification-system" aria-live="polite">
      {notifications.map((n) => (
        <div key={n.id} className="notification" role="alert">
          <strong className="notification-title">{n.title}</strong>
          <p className="notification-body">{n.body}</p>
          <button
            type="button"
            className="notification-dismiss"
            aria-label="Dismiss notification"
            onClick={() => dismiss(n.id)}
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}

NotificationSystem.propTypes = {
  initialNotifications: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      body: PropTypes.string.isRequired,
    })
  ),
};

export default NotificationSystem;