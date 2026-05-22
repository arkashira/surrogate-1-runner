import { RemediationAction } from '../types/remediation';

export interface NotificationConfig {
  emailEnabled: boolean;
  slackEnabled: boolean;
  webhookUrl?: string;
  retryAttempts?: number; // Added for reliability
  timeout?: number; // Added for performance
}

export class NotificationService {
  private config: NotificationConfig;
  private readonly defaultRetryAttempts = 3;
  private readonly defaultTimeout = 5000;

  constructor(config: NotificationConfig) {
    this.config = {
      ...config,
      retryAttempts: config.retryAttempts ?? this.defaultRetryAttempts,
      timeout: config.timeout ?? this.defaultTimeout
    };
  }

  async sendRemediationNotification(action: RemediationAction): Promise<void> {
    const message = this.buildRemediationMessage(action);

    const notifications = [];

    if (this.config.emailEnabled) {
      notifications.push(this.sendEmailNotification(message));
    }

    if (this.config.slackEnabled) {
      notifications.push(this.sendSlackNotification(message));
    }

    if (this.config.webhookUrl) {
      notifications.push(this.sendWebhookNotification(message));
    }

    // Parallel execution with error handling
    await Promise.allSettled(notifications);
  }

  private buildRemediationMessage(action: RemediationAction): string {
    return `Automated remediation triggered:
    - Type: ${action.type}
    - Resource ID: ${action.resourceId}
    - Policy: ${action.policyName}
    - Reason: ${action.reason}
    - Status: ${action.status}
    - Timestamp: ${new Date().toISOString()}`;
  }

  private async sendEmailNotification(message: string): Promise<void> {
    try {
      // Implementation would integrate with email service
      console.log(`[EMAIL] Sending notification: ${message}`);
      // Add retry logic for production
      // await this.retryOperation(() => actualEmailService.send(message));
    } catch (error) {
      console.error('Email notification failed:', error);
      throw error;
    }
  }

  private async sendSlackNotification(message: string): Promise<void> {
    try {
      // Implementation would integrate with Slack API
      console.log(`[SLACK] Sending notification: ${message}`);
      // Add retry logic for production
    } catch (error) {
      console.error('Slack notification failed:', error);
      throw error;
    }
  }

  private async sendWebhookNotification(message: string): Promise<void> {
    if (!this.config.webhookUrl) return;

    try {
      // Implementation would send to configured webhook
      console.log(`[WEBHOOK] Sending notification to ${this.config.webhookUrl}`);
      // Add timeout and retry logic for production
    } catch (error) {
      console.error('Webhook notification failed:', error);
      throw error;
    }
  }

  // Helper method for retry logic
  private async retryOperation<T>(
    operation: () => Promise<T>,
    maxRetries: number = this.config.retryAttempts!
  ): Promise<T> {
    let lastError: unknown;

    for (let i = 0; i < maxRetries; i++) {
      try {
        return await Promise.race([
          operation(),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Operation timed out')), this.config.timeout)
          )
        ]);
      } catch (error) {
        lastError = error;
        if (i < maxRetries - 1) {
          await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
      }
    }

    throw lastError;
  }
}