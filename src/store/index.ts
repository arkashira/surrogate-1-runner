import { configureStore } from '@reduxjs/toolkit';
import rulesReducer from './rulesSlice';

export const store = configureStore({
  reducer: {
    rules: rulesReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;