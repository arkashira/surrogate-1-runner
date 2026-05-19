import axios from 'axios';

const API_BASE = '/api/deals';

const dealService = {
  /**
   * Fetch all active investment matches.
   * @returns {Promise<Array>}
   */
  fetchActiveMatches: async () => {
    try {
      const response = await axios.get(`${API_BASE}/active`);
      return response.data;
    } catch (error) {
      console.error('Error fetching matches:', error);
      throw error; // Re-throw so component can handle UI state
    }
  },

  /**
   * Update the status of a specific match.
   * @param {string} matchId 
   * @param {string} newStatus 
   */
  updateMatchStatus: async (matchId, newStatus) => {
    try {
      const response = await axios.patch(`${API_BASE}/${matchId}`, {
        status: newStatus,
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating match ${matchId}:`, error);
      throw error;
    }
  },

  /**
   * Optional: Explicitly send a notification to the backend
   */
  sendNotification: async (matchId, newStatus) => {
    try {
      await axios.post('/api/notifications', {
        matchId,
        status: newStatus,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Error sending notification:', error);
      // Non-critical, so we might not throw here depending on requirements
    }
  },
};

export default dealService;