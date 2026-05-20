import { SET_PROVIDER } from './types';

export const setProvider = (provider: string) => ({
  type: SET_PROVIDER,
  payload: provider,
});