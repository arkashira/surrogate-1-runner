import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { fetchNotifications, acknowledgeNotification } from '../actions/notificationActions';

const NotificationSystem: React.FC = () => {
  const dispatch = useDispatch();
  const notifications = useSelector((state: RootState) => state.notifications.notifications);
  const [visibleNotifications, setVisibleNotifications] = useState<any[]>([]);

  useEffect(() => {
    dispatch(fetchNotifications());
  }, [dispatch]);

  useEffect(() => {
    setVisibleNotifications(notifications.filter(notification => !notification.acknowledged));
  }, [notifications]);

  const handleAcknowledge = (id: string) => {
    dispatch(acknowledgeNotification(id));
  };

  return (
    <div className="notification-system">
      {visibleNotifications.map(notification => (
        <div key={notification.id} className="notification">
          <div className="notification-content">
            <h4>{notification.title}</h4>
            <p>{notification.message}</p>
          </div>
          <button onClick={() => handleAcknowledge(notification.id)}>Acknowledge</button>
        </div>
      ))}
    </div>
  );
};

export default NotificationSystem;