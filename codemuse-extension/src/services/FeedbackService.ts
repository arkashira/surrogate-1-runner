import axios, { AxiosError } from 'axios';

export class FeedbackService {
  private readonly apiBaseUrl: string;

  constructor(apiBaseUrl: string) {
    this.apiBaseUrl = apiBaseUrl;
  }

  async sendFeedback(suggestionId: string, rating: 'up' | 'down'): Promise<void> {
    const endpoint = `${this.apiBaseUrl}/api/v1/suggestions/${suggestionId}/feedback`;
    try {
      await axios.post(endpoint, {
        rating: rating,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
    } catch (error) {
      if (error instanceof AxiosError) {
        console.error(`Failed to send feedback for suggestion ${suggestionId}:`, error.response?.data || error.message);
      } else {
        console.error(`Unexpected error sending feedback:`, error);
      }
    }
  }
}