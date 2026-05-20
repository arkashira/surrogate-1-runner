import { configureStore } from '@reduxjs/toolkit';
import sandboxReducer from '../features/sandbox/sandboxSlice';

export const store = configureStore({
  reducer: {
    sandbox: sandboxReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;