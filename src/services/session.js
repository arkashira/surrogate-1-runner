import axios from 'axios';

export const terminateSession = async () => {
  try {
    await axios.post('/api/session/terminate');
  } catch (error) {
    console.error('Error terminating session:', error);
  }
};