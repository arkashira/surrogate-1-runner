const fetchForecastData = async (timeRange) => {
  // In a real application, this would be an API call to your backend service
  // For this example, we'll return mock data
  const mockData = {
    '30-day': [
      { date: '2023-05-01', cashFlow: 1000 },
      { date: '2023-05-02', cashFlow: 1500 },
      { date: '2023-05-03', cashFlow: 1200 },
      // ... more data points
    ],
    '90-day': [
      { date: '2023-05-01', cashFlow: 1000 },
      { date: '2023-05-02', cashFlow: 1500 },
      { date: '2023-05-03', cashFlow: 1200 },
      // ... more data points
    ],
  };

  return mockData[timeRange];
};

export { fetchForecastData };