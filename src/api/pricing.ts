import axios from 'axios';

export interface PricingItem {
  date: string;          // ISO date string
  category: string;
  product: string;
  competitor: string;
  price: number;
}

export const fetchPricingData = async (): Promise<PricingItem[]> => {
  const { data } = await axios.get<PricingItem[]>('/api/pricing-analysis');
  return data;
};