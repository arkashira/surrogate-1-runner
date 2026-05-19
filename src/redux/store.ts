import { configureStore } from '@reduxjs/toolkit';
import { dealFlowApi } from './dealFlowApiSlice';

export const store = configureStore({
  reducer: {
    [dealFlowApi.reducerPath]: dealFlowApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(dealFlowApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;