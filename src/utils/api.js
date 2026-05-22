import axios from 'axios';

const API_URL = 'https://api.example.com/components';

const fetchComponentDetails = async (id) => {
  const response = await axios.get(`${API_URL}/${id}`);
  return response.data;
};

export { fetchComponentDetails };