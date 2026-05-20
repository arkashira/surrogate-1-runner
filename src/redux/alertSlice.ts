import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AlertState } from './types';

const initialState: AlertState = {
  threshold: 20,
  notificationMethod: 'email',
};

export const alertSlice = createSlice({
  name: 'alert',
  initialState,
  reducers: {
    setThreshold(state, action: PayloadAction<number>) {
      state.threshold = action.payload;
    },
    setNotificationMethod(state, action: PayloadAction<AlertState['notificationMethod']>) {
      state.notificationMethod = action.payload;
    },
  },
});

export const { setThreshold, setNotificationMethod } = alertSlice.actions;
export default alertSlice.reducer;