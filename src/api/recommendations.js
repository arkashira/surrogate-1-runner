export const fetchRecommendations = async () => {
  try {
    // Simulate API call to fetch recommendations
    const response = await fetch('/api/recommendations');
    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};