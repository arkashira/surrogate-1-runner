import { Injectable } from '@nestjs/common';
import { Cron } from 'node-cron';
import { WorkflowService } from './WorkflowService';
import { Job } from './Job';

@Injectable()
export class SchedulerService {
  private jobQueue: Job[] = [];
  private cron: Cron;

  constructor(private workflowService: WorkflowService) {
    this.cron = new Cron('* * * * *', () => this.executeQueuedJobs());
  }

  async scheduleJob(job: Job) {
    this.jobQueue.push(job);
    this.cron.schedule('* * * * *', () => this.executeQueuedJobs());
  }

  private async executeQueuedJobs() {
    const now = new Date();
    const jobsToExecute = this.jobQueue.filter((job) => job.timestamp <= now);
    this.jobQueue = this.jobQueue.filter((job) => job.timestamp > now);

    for (const job of jobsToExecute) {
      try {
        await this.workflowService.triggerWorkflow(job.workflowId);
        console.log(`Job ${job.id} executed successfully`);
      } catch (error) {
        console.error(`Error executing job ${job.id}: ${error.message}`);
      }
    }
  }
}