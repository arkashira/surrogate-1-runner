import axios from 'axios';
import { APIResponse, AxentxError } from '../types';

export class DecisionMakingToolAPI {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  async getAlerts(): Promise<APIResponse> {
    try {
      const response = await axios.get(`${this.baseURL}/alerts`);
      return response.data;
    } catch (error) {
      throw new AxentxError('Failed to fetch alerts', error);
    }
  }

  async getArtifacts(): Promise<APIResponse> {
    try {
      const response = await axios.get(`${this.baseURL}/artifacts`);
      return response.data;
    } catch (error) {
      throw new AxentxError('Failed to fetch artifacts', error);
    }
  }
}