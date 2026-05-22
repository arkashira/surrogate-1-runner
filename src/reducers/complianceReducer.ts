import {
  FETCH_COMPLIANCE_ISSUES_REQUEST,
  FETCH_COMPLIANCE_ISSUES_SUCCESS,
  FETCH_COMPLIANCE_ISSUES_FAILURE,
} from '../actions/complianceActions';
import { ComplianceIssue } from '../types/complianceTypes';

interface ComplianceState {
  issues: ComplianceIssue[];
  loading: boolean;
  error: string | null;
}

const initialState: ComplianceState = {
  issues: [],
  loading: false,
  error: null,
};

const complianceReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case FETCH_COMPLIANCE_ISSUES_REQUEST:
      return {
        ...state,
        loading: true,
        error: null,
      };
    case FETCH_COMPLIANCE_ISSUES_SUCCESS:
      return {
        ...state,
        loading: false,
        issues: action.payload,
      };
    case FETCH_COMPLIANCE_ISSUES_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    default:
      return state;
  }
};

export default complianceReducer;