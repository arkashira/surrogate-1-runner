import { Injectable } from '@nestjs/common';

@Injectable()
export class WorkflowService {
  async triggerWorkflow(workflowId: string) {
    // TO DO: implement workflow triggering logic
    console.log(`Triggering workflow ${workflowId}`);
  }
}