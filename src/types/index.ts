export interface InvestorCriteria {
  industry: string;
  fundingStage: string;
  geographicFocus: string;
}

export interface InvestorCriteriaFormData extends InvestorCriteria {
  isValid: boolean;
}