import { combineReducers } from 'redux';
import complianceReducer from './complianceReducer';

const rootReducer = combineReducers({
  compliance: complianceReducer,
});

export type RootState = ReturnType<typeof rootReducer>;
export default rootReducer;