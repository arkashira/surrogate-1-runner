import { Dispatch } from 'redux';
import { ThunkAction } from 'redux-thunk';
import { RootState } from '../store';
import { Notification } from '../types';

export const FETCH_NOTIFICATIONS = 'FETCH_NOTIFICATIONS';
export const ACKNOWLEDGE_NOTIFICATION = 'ACKNOWLEDGE_NOTIFICATION';

export const fetchNotifications = (): ThunkAction<void, RootState, unknown, any> => async (dispatch: Dispatch) => {
  try {
    const response = await fetch('/api/notifications');
    const data: Notification[] = await response.json();
    dispatch({ type: FETCH_NOTIFICATIONS, payload: data });
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
};

export const acknowledgeNotification = (id: string): ThunkAction<void, RootState, unknown, any> => async (dispatch: Dispatch) => {
  try {
    await fetch(`/api/notifications/${id}/acknowledge`, { method: 'POST' });
    dispatch({ type: ACKNOWLEDGE_NOTIFICATION, payload: id });
  } catch (error) {
    console.error('Error acknowledging notification:', error);
  }
};