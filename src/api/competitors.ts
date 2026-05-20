import axios from 'axios';

export const fetchCompetitors = async (): Promise<string[]> => {
  const { data } = await axios.get<string[]>('/api/competitors');
  return data;
};