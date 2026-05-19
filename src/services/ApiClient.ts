import { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

interface ApiClientOptions {
  baseURL: string;
  timeout?: number;
}

class ApiClient {
  private baseURL: string;
  private timeout: number;

  constructor(options: ApiClientOptions) {
    this.baseURL = options.baseURL;
    this.timeout = options.timeout || 5000;
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    // Configure request with timeout
    const config: AxiosRequestConfig = {
      method: 'POST',
      url,
      data,
      timeout: this.timeout,
    };

    // Retry logic with max 2 retries
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt <= 2; attempt++) {
      try {
        const response: AxiosResponse<T> = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
          signal: AbortSignal.timeout(this.timeout),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result: T = await response.json();
        return result;
      } catch (error) {
        lastError = error instanceof Error ? error : new Error('Unknown error occurred');
        
        // Don't retry on the last attempt
        if (attempt >= 2) {
          break;
        }
        
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }

    // Throw the last error after all retries exhausted
    throw lastError || new Error('Failed to get response after all retries');
  }
}

export default ApiClient;