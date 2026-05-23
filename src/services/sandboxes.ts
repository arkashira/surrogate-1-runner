import axios, { AxiosError } from 'axios';

const EXTERNAL_API_URL = process.env.SANDBOX_API_URL || 'https://api.example.com';

interface ApiError extends Error {
  response?: {
    status: number;
    data?: unknown;
  };
}

const deleteSandbox = async (sandboxId: string): Promise<void> => {
  try {
    await axios.delete(`${EXTERNAL_API_URL}/sandboxes/${sandboxId}`);
  } catch (error) {
    const axiosError = error as AxiosError;
    
    if (axiosError.response?.status === 404) {
      throw new Error(`Sandbox not found: ${sandboxId}`);
    }
    
    if (axiosError.response?.status === 403) {
      throw new Error('Unauthorized to delete this sandbox');
    }
    
    throw new Error(`Failed to delete sandbox: ${axiosError.message}`);
  }
};

export { deleteSandbox };