import { PushNotificationService } from '@nestjs/push-notifications';

export class PushNotificationService {
  async sendNotification(message: string) {
    // TO DO: implement push notification logic
    console.log(`Sending push notification: ${message}`);
  }
}