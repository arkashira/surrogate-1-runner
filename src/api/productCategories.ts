import axios from 'axios';

export const fetchProductCategories = async (): Promise<string[]> => {
  const { data } = await axios.get<string[]>('/api/product-categories');
  return data;
};