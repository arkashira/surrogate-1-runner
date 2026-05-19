import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { Deal } from '../types/deal';

export const dealFlowApi = createApi({
  reducerPath: 'dealFlowApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    getDealFlow: builder.query<Deal[], void>({
      query: () => '/deal-flow',
    }),
  }),
});

export const { useGetDealFlowQuery } = dealFlowApi;