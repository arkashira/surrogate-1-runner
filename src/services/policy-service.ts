import axios from 'axios';

interface Policy {
  name: string;
  maxInstanceSize: string;
  idleTimeout: string;
}

interface PolicyService {
  createPolicy(policy: Policy): Promise<any>;
}

const policyService: PolicyService = {
  async createPolicy(policy: Policy) {
    try {
      const response = await axios.post('/api/policies', policy);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default policyService;