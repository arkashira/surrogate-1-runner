import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import NotificationSystem from './NotificationSystem';

const middlewares = [thunk];
const mockStore = configureStore(middlewares);

describe('NotificationSystem', () => {
  it('renders notifications and handles acknowledgment', () => {
    const initialState = {
      notifications: {
        notifications: [
          { id: '1', title: 'Test Notification', message: 'This is a test notification', acknowledged: false },
        ],
      },
    };

    const store = mockStore(initialState);

    const { getByText } = render(
      <Provider store={store}>
        <NotificationSystem />
      </Provider>
    );

    expect(getByText('Test Notification')).toBeInTheDocument();
    expect(getByText('This is a test notification')).toBeInTheDocument();

    fireEvent.click(getByText('Acknowledge'));

    const actions = store.getActions();
    expect(actions).toContainEqual({ type: 'ACKNOWLEDGE_NOTIFICATION', payload: '1' });
  });
});