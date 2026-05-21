import axios from 'axios';
import { Finding } from '../types';

const API_BASE_URL = 'https://api.example.com';

export const getFindings = async (): Promise<Finding[]> => {
  const response = await axios.get(`${API_BASE_URL}/findings`);
  return response.data;
};

export const getFindingById = async (id: string): Promise<Finding> => {
  const response = await axios.get(`${API_BASE_URL}/findings/${id}`);
  return response.data;
};