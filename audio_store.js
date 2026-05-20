import { createStore } from 'redux';
import audioReducer from './audio_reducer';

const store = createStore(
  audioReducer,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

export default store;