export const SET_PASSCODE = 'SET_PASSCODE';
export const INCREMENT_RETRY_COUNT = 'INCREMENT_RETRY_COUNT';
export const RESET_RETRY_COUNT = 'RESET_RETRY_COUNT';

export const setPasscode = (passcode) => ({
  type: SET_PASSCODE,
  payload: passcode,
});

export const incrementRetryCount = () => ({
  type: INCREMENT_RETRY_COUNT,
});

export const resetRetryCount = () => ({
  type: RESET_RETRY_COUNT,
});