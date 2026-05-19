import axios, { AxiosResponse } from 'axios';

export interface SuggestionRequest {
  context: string;
}

export interface SuggestionResponse {
  suggestions: string[];
}

export class ApiClient {
  private readonly API_URL = 'https://api.surrogate-1.com/suggestions';

  async getSuggestions(request: SuggestionRequest): Promise<SuggestionResponse> {
    try {
      const response: AxiosResponse<SuggestionResponse> = await axios.post(
        this.API_URL,
        request
      );
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch suggestions. Please try again later.');
    }
  }
}