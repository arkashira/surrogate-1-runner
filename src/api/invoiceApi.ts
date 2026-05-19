import axios from 'axios';
import { InvoiceSummary } from '../types';

const API_URL = 'https://api.example.com/invoices';

export const fetchInvoiceSummaries = async (): Promise<InvoiceSummary[]> => {
  try {
    const response = await axios.get(`${API_URL}/summaries`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch invoice summaries');
  }
};