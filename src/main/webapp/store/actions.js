actions: {
  async fetchRemediations({ commit, state }) {
    try {
      const response = await axios.get('/api/remediations');
      const remediationMap = {};
      
      response.data.forEach(remediation => {
        remediationMap[remediation.vulnerability_id] = remediation;
      });
      
      commit('SET_REMEDIATIONS', {
        vulnerabilities: state.vulnerabilities.map(vuln => ({
          ...vuln,
          remediation: remediationMap[vuln.id] || {
            steps: [{ 
              description: 'No specific remediation available',
              command: null
            }]
          })
        })
      });
    } catch (error) {
      console.error('Failed to fetch remediations:', error);
      commit('SET_REMEDIATIONS', { 
        vulnerabilities: state.vulnerabilities.map(vuln => ({
          ...vuln,
          remediation: {
            steps: [{ 
              description: 'Failed to load remediation data',
              command: null
            }]
          }
        }))
      });
    }
  }
}