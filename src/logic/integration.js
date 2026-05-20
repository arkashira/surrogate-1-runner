const axios = require('axios');

/**
 * IntegrationManager handles communication with an external IT service.
 * It is deliberately lightweight: it only knows how to test connectivity
 * and expose the current configuration.
 */
class IntegrationManager {
  /**
   * @param {{endpoint:string, username:string, password:string}} config
   */
  constructor(config) {
    this.config = { ...config };
  }

  /**
   * Returns the current integration configuration (excluding the password
   * for safety when logging).
   */
  getConfig() {
    const { password, ...safeConfig } = this.config;
    return safeConfig;
  }

  /**
   * Tests the external service connectivity.
   * Returns a boolean indicating success.
   */
  async testConnection() {
    const { endpoint, username, password } = this.config;
    if (!endpoint || !username || !password) {
      return false;
    }

    try {
      const response = await axios.get(endpoint, {
        timeout: 5000,
        auth: {
          username,
          password,
        },
        // Do not log request/response bodies – keep it secure.
        validateStatus: (status) => status >= 200 && status < 300,
      });
      return response.status === 200;
    } catch (_) {
      return false;
    }
  }
}

module.exports = IntegrationManager;