import { InvestorCriteria } from '../../types';

export const SET_INVESTOR_CRITERIA = 'SET_INVESTOR_CRITERIA';
export const SET_INVESTOR_CRITERIA_LOADING = 'SET_INVESTOR_CRITERIA_LOADING';
export const SET_INVESTOR_CRITERIA_ERROR = 'SET_INVESTOR_CRITERIA_ERROR';

export const setInvestorCriteria = (criteria: InvestorCriteria) => ({
  type: SET_INVESTOR_CRITERIA,
  payload: criteria,
});

export const setInvestorCriteriaLoading = (isLoading: boolean) => ({
  type: SET_INVESTOR_CRITERIA_LOADING,
  payload: isLoading,
});

export const setInvestorCriteriaError = (error: string | null) => ({
  type: SET_INVESTOR_CRITERIA_ERROR,
  payload: error,
});