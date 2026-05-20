import axios from 'axios';

interface ValidationResult {
  isValid: boolean;
  message: string;
}

export class ProviderValidationService {
  private axiosInstance = axios.create({
    timeout: 10000,
  });

  /**
   * Validates AWS credentials by attempting to list S3 buckets.
   * @param accessKeyId AWS access key ID
   * @param secretAccessKey AWS secret access key
   * @returns Validation result
   */
  async validateAwsCredentials({
    accessKeyId,
    secretAccessKey,
  }: {
    accessKeyId: string;
    secretAccessKey: string;
  }): Promise<ValidationResult> {
    try {
      const response = await this.axiosInstance.get(
        'https://s3.amazonaws.com',
        {
          headers: {
            'Authorization': `AWS ${accessKeyId}:${secretAccessKey}`,
          },
        }
      );
      return { isValid: true, message: 'AWS credentials are valid' };
    } catch (error) {
      return { isValid: false, message: 'AWS credentials are invalid' };
    }
  }

  /**
   * Validates GCP credentials by attempting to list storage buckets.
   * @param serviceAccountKey GCP service account JSON key
   * @returns Validation result
   */
  async validateGcpCredentials({
    serviceAccountKey,
  }: {
    serviceAccountKey: string;
  }): Promise<ValidationResult> {
    try {
      const response = await this.axiosInstance.post(
        'https://www.googleapis.com/storage/v1/b',
        {},
        {
          headers: {
            'Authorization': `Bearer ${serviceAccountKey}`,
          },
        }
      );
      return { isValid: true, message: 'GCP credentials are valid' };
    } catch (error) {
      return { isValid: false, message: 'GCP credentials are invalid' };
    }
  }

  /**
   * Validates Azure credentials by attempting to list storage accounts.
   * @param subscriptionId Azure subscription ID
   * @param clientId Azure client ID
   * @param clientSecret Azure client secret
   * @param tenantId Azure tenant ID
   * @returns Validation result
   */
  async validateAzureCredentials({
    subscriptionId,
    clientId,
    clientSecret,
    tenantId,
  }: {
    subscriptionId: string;
    clientId: string;
    clientSecret: string;
    tenantId: string;
  }): Promise<ValidationResult> {
    try {
      const response = await this.axiosInstance.post(
        'https://management.azure.com/subscriptions',
        {},
        {
          headers: {
            'Authorization': `Bearer ${clientId}:${clientSecret}`,
          },
        }
      );
      return { isValid: true, message: 'Azure credentials are valid' };
    } catch (error) {
      return { isValid: false, message: 'Azure credentials are invalid' };
    }
  }
}