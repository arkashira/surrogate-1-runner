import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import invoiceReducer from '../reducers/invoiceReducer';

const rootReducer = combineReducers({
  invoice: invoiceReducer,
});

export type RootState = ReturnType<typeof rootReducer>;

const store = createStore(rootReducer, applyMiddleware(thunk));

export default store;