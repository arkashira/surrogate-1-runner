import { Dispatch } from 'redux';
import { ComplianceIssue } from '../types/complianceTypes';
import { fetchComplianceIssues as fetchComplianceIssuesAPI } from '../api/complianceApi';

export const FETCH_COMPLIANCE_ISSUES_REQUEST = 'FETCH_COMPLIANCE_ISSUES_REQUEST';
export const FETCH_COMPLIANCE_ISSUES_SUCCESS = 'FETCH_COMPLIANCE_ISSUES_SUCCESS';
export const FETCH_COMPLIANCE_ISSUES_FAILURE = 'FETCH_COMPLIANCE_ISSUES_FAILURE';

export const fetchComplianceIssues = () => {
  return async (dispatch: Dispatch) => {
    dispatch({ type: FETCH_COMPLIANCE_ISSUES_REQUEST });

    try {
      const issues: ComplianceIssue[] = await fetchComplianceIssuesAPI();
      dispatch({ type: FETCH_COMPLIANCE_ISSUES_SUCCESS, payload: issues });
    } catch (error) {
      dispatch({ type: FETCH_COMPLIANCE_ISSUES_FAILURE, payload: error.message });
    }
  };
};