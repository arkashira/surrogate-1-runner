import { Notification } from '../types';
import { FETCH_NOTIFICATIONS, ACKNOWLEDGE_NOTIFICATION } from '../actions/notificationActions';

interface NotificationState {
  notifications: Notification[];
}

const initialState: NotificationState = {
  notifications: [],
};

const notificationReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case FETCH_NOTIFICATIONS:
      return {
        ...state,
        notifications: action.payload,
      };
    case ACKNOWLEDGE_NOTIFICATION:
      return {
        ...state,
        notifications: state.notifications.map(notification =>
          notification.id === action.payload ? { ...notification, acknowledged: true } : notification
        ),
      };
    default:
      return state;
  }
};

export default notificationReducer;