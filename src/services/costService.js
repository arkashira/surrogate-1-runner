import axios from 'axios';

class CostService {
  async getCostData(projectId, resourceType) {
    const url = `https://billingexport.googleapis.com/v1/projects/${projectId}/costs?resourceType=${resourceType}`;
    const response = await axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_GCP_BILLING_EXPORT_API_KEY',
      },
    });
    return response.data;
  }
}

export default CostService;