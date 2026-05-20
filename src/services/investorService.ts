import { InvestorCriteria } from '../types';

const STORAGE_KEY = 'investor_criteria';

// Simulate API call with localStorage persistence
export const investorService = {
  saveCriteria: async (criteria: InvestorCriteria): Promise<InvestorCriteria> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(criteria));
    return criteria;
  },

  loadCriteria: async (): Promise<InvestorCriteria | null> => {
    await new Promise(resolve => setTimeout(resolve, 200));
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : null;
  },

  validateCriteria: (criteria: Partial<InvestorCriteria>): string[] => {
    const errors: string[] = [];
    if (!criteria.industry?.trim()) errors.push('Industry is required');
    if (!criteria.fundingStage?.trim()) errors.push('Funding stage is required');
    if (!criteria.geographicFocus?.trim()) errors.push('Geographic focus is required');
    return errors;
  },
};