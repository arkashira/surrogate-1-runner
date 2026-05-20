import { createStore } from 'vuex';
import { alerts } from './modules/alerts';

export interface RootState {}

export default createStore<RootState>({
  modules: {
    alerts,
  },
});