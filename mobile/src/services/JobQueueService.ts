import NotificationHelper from '../utils/NotificationHelper';

class JobQueueService {
  private jobQueue: Array<{ id: string; timestamp: Date; workflow: any }> = [];

  constructor() {
    NotificationHelper.initialize();
  }

  addJob(job: { id: string; timestamp: Date; workflow: any }) {
    this.jobQueue.push(job);
    this.processQueue();
  }

  private async processQueue() {
    if (this.jobQueue.length === 0) return;

    const job = this.jobQueue[0];
    try {
      await this.executeJob(job);
      this.jobQueue.shift();
      NotificationHelper.scheduleJobCompletionNotification(
        job.id,
        'Job Completed',
        `Workflow ${job.workflow.name} has completed successfully.`
      );
    } catch (error) {
      console.error('Error executing job:', error);
    } finally {
      this.processQueue();
    }
  }

  private async executeJob(job: { id: string; timestamp: Date; workflow: any }) {
    // Implement job execution logic here
    console.log(`Executing job ${job.id} for workflow ${job.workflow.name}`);
    // Simulate job execution
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

export default JobQueueService;