import { store } from './index';
import { RootState } from './index';

const STORAGE_KEY = 'formattingRules';

store.subscribe(() => {
  const state: RootState = store.getState();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.rules));
});