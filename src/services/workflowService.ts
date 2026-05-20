import axios from 'axios';

const API_URL = 'https://api.example.com/workflows';

export const createWorkflow = async (workflowData: any) => {
  const response = await axios.post(API_URL, workflowData);
  return response.data;
};

export const getWorkflows = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const executeWorkflow = async (id: string) => {
  const response = await axios.post(`${API_URL}/${id}/execute`);
  return response.data;
};