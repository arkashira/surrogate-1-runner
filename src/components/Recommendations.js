
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch recommendations from an API endpoint
    const fetchRecommendations = async () => {
      try {
        const response = await axios.get('/api/recommendations');
        setRecommendations(response.data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      }
    };

    fetchRecommendations();
  }, []);

  const applyRecommendation = async (recId) => {
    setLoading(true);
    try {
      await axios.post(`/api/recommendations/${recId}/apply`);
      // Remove the applied recommendation from the list
      setRecommendations(prevRecs => prevRecs.filter(rec => rec.id !== recId));
    } catch (error) {
      console.error(`Error applying recommendation ${recId}:`, error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Cloud Spending Optimization Recommendations</h1>
      <p>Below are the latest automated recommendations. Click "Apply" to implement immediately.</p>
      <table>
        <thead>
          <tr>
            <th>Recommendation ID</th>
            <th>Description</th>
            <th>Estimated Savings</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {recommendations.map(rec => (
            <tr key={rec.id}>
              <td>{rec.id}</td>
              <td>{rec.description}</td>
              <td>{rec.estimatedSavings}</td>
              <td>
                <button
                  className="apply-btn"
                  onClick={() => applyRecommendation(rec.id)}
                  disabled={loading}
                >
                  {loading ? 'Applying...' : 'Apply'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Recommendations;