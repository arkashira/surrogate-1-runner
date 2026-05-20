export class Job {
  id: string;
  timestamp: Date;
  workflowId: string;

  constructor(id: string, timestamp: Date, workflowId: string) {
    this.id = id;
    this.timestamp = timestamp;
    this.workflowId = workflowId;
  }
}