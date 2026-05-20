import axios from 'axios';

const complianceReportService = {
  getComplianceReport: async () => {
    try {
      const response = await axios.get('/api/compliance-report');
      return response.data;
    } catch (error) {
      console.error(error);
      return null;
    }
  },
};

export default complianceReportService;