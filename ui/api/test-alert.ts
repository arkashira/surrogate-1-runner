import axios from 'axios';

const sendTestAlert = async () => {
  try {
    await axios.post('/api/test-alert');
  } catch (error) {
    console.error(error);
  }
};

export { sendTestAlert };