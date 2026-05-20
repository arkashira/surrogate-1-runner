import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import PasscodeInput from '../components/PasscodeInput';

const mockStore = configureStore([]);

describe('PasscodeInput', () => {
  let store;

  beforeEach(() => {
    store = mockStore({
      retryCount: 0,
    });
  });

  it('renders correctly', () => {
    const { getByPlaceholderText, getByText } = render(
      <Provider store={store}>
        <PasscodeInput />
      </Provider>
    );

    expect(getByPlaceholderText('Enter your passcode')).toBeInTheDocument();
    expect(getByText('Submit')).toBeInTheDocument();
  });

  it('dispatches setPasscode action on form submit', () => {
    const { getByPlaceholderText, getByText } = render(
      <Provider store={store}>
        <PasscodeInput />
      </Provider>
    );

    fireEvent.change(getByPlaceholderText('Enter your passcode'), { target: { value: 'testpasscode' } });
    fireEvent.click(getByText('Submit'));

    expect(store.getActions()).toContainEqual({ type: 'SET_PASSCODE', payload: 'testpasscode' });
  });
});