import { SET_PASSCODE, INCREMENT_RETRY_COUNT, RESET_RETRY_COUNT } from './actions';

const initialState = {
  passcode: '',
  retryCount: 0,
};

const rootReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_PASSCODE:
      return {
        ...state,
        passcode: action.payload,
      };
    case INCREMENT_RETRY_COUNT:
      return {
        ...state,
        retryCount: state.retryCount + 1,
      };
    case RESET_RETRY_COUNT:
      return {
        ...state,
        retryCount: 0,
      };
    default:
      return state;
  }
};

export default rootReducer;