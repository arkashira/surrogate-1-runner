import { Platform } from 'react-native';
import PushNotification from 'react-native-push-notification';

class NotificationHelper {
  static initialize() {
    PushNotification.configure({
      onNotification: function (notification) {
        console.log('NOTIFICATION:', notification);
      },
      popInitialNotification: true,
      requestPermissions: true,
    });
  }

  static scheduleJobCompletionNotification(jobId: string, title: string, message: string) {
    PushNotification.localNotificationSchedule({
      message: message,
      date: new Date(Date.now() + 1000), // Notify after 1 second (adjust as needed)
      userInfo: {
        jobId: jobId,
        type: 'job_completion',
      },
      playSound: true,
      soundName: 'default',
      channelId: Platform.OS === 'android' ? 'job-completion-channel' : undefined,
    });
  }
}

export default NotificationHelper;