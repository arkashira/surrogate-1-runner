+ import { notifyStatusChangeQueue } from '../jobs/notifyStatusChange';

  export class RequestService {
    // ... existing code

-   // old status change logic (example)
-   async updateStatus(requestId: string, newStatus: string) {
-     const request = await this.requestRepo.findById(requestId);
-     request.status = newStatus;
-     await this.requestRepo.save(request);
-   }

+   async updateStatus(requestId: string, newStatus: string, channel?: string) {
+     const request = await this.requestRepo.findById(requestId);
+     const previousStatus = request.status;
+     request.status = newStatus;
+     await this.requestRepo.save(request);
+
+     // Enqueue notification job
+     await notifyStatusChangeQueue.add('notify-status-change', {
+       requestId,
+       channel: channel || process.env.SLACK_DEFAULT_CHANNEL || 'status-updates',
+       previousStatus,
+       newStatus,
+     }, {
+       attempts: 3,
+       backoff: { type: 'exponential', delay: 2000 },
+       removeOnComplete: 100,
+       removeOnFail: 50,
+     });
+   }
  }