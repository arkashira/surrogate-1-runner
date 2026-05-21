import axios from 'axios';

interface Agent {
  id: string;
  name: string;
  status: string;
}

interface Workflow {
  id: string;
  name: string;
  status: string;
  agents: Agent[];
}

export const fetchWorkflows = async (): Promise<Workflow[]> => {
  try {
    const response = await axios.get('/api/workflows');
    return response.data;
  } catch (error) {
    console.error('Error fetching workflows:', error);
    return [];
  }
};