import { 
  SET_INVESTOR_CRITERIA, 
  SET_INVESTOR_CRITERIA_LOADING, 
  SET_INVESTOR_CRITERIA_ERROR 
} from '../actions/investorActions';
import { InvestorCriteria } from '../../types';

interface InvestorState {
  investorCriteria: InvestorCriteria;
  isLoading: boolean;
  error: string | null;
}

const initialState: InvestorState = {
  investorCriteria: {
    industry: '',
    fundingStage: '',
    geographicFocus: '',
  },
  isLoading: false,
  error: null,
};

const investorReducer = (state = initialState, action: any): InvestorState => {
  switch (action.type) {
    case SET_INVESTOR_CRITERIA:
      return {
        ...state,
        investorCriteria: action.payload,
        error: null,
      };
    case SET_INVESTOR_CRITERIA_LOADING:
      return{
        ...state,
        isLoading: action.payload,
      };
    case SET_INVESTOR_CRITERIA_ERROR:
      return{
        ...state,
        error: action.payload,
      };
    default:
      return state;
  }
};

export default investorReducer;