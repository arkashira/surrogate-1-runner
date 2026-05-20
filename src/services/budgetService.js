import axios from 'axios';

const budgetService = {
  getHistoricalData: async () => {
    const response = await axios.get('/api/historical-data');
    return response.data;
  },

  getForecast: async (data) => {
    const response = await axios.post('/api/forecast', { data });
    return response.data;
  },

  adjustForecastParams: async (params) => {
    const response = await axios.post('/api/adjust-forecast-params', { params });
    return response.data;
  },
};

export default budgetService;