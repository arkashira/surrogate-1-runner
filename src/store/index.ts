import { configureStore } from '@reduxjs/toolkit';
import costAlertReducer from './costAlertSlice';

export const store = configureStore({
  reducer: {
    costAlert: costAlertReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;