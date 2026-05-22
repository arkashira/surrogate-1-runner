import axios from 'axios';
import { ComplianceIssue } from '../types/complianceTypes';

const API_BASE_URL = 'https://api.example.com';

export const fetchComplianceIssues = async (): Promise<ComplianceIssue[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/compliance-issues`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch compliance issues');
  }
};