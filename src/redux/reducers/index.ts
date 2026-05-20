import { combineReducers } from 'redux';
import providerReducer from './providerReducer';

export const rootReducer = combineReducers({
  provider: providerReducer,
});

export type RootState = ReturnType<typeof rootReducer>;