import { SET_PROVIDER } from '../actions/types';

const initialState = {
  currentProvider: 'openai',
};

export default function providerReducer(state = initialState, action: any) {
  switch (action.type) {
    case SET_PROVIDER:
      return {
        ...state,
        currentProvider: action.payload,
      };
    default:
      return state;
  }
}