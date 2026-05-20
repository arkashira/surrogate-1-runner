import { openDB, IDBPDatabase } from 'idb';
import { Workflow, StepResult } from '../models';
import { executeStep } from '../utils/executeStep';

const DB_NAME = 'workflow-db';
const WORKFLOW_STORE = 'workflows';
const RESULT_STORE = 'results';

export class OfflineWorkflowEngine {
  private db!: IDBPDatabase;
  private syncQueue: StepResult[] = [];

  async init(): Promise<void> {
    this.db = await openDB(DB_NAME, 1, {
      upgrade(db) {
        db.createObjectStore(WORKFLOW_STORE, { keyPath: 'id' });
        db.createObjectStore(RESULT_STORE, { keyPath: 'stepId' });
      },
    });
  }

  async addWorkflow(workflow: Workflow): Promise<void> {
    await this.db.put(WORKFLOW_STORE, workflow);
  }

  async getWorkflow(id: string): Promise<Workflow | undefined> {
    return this.db.get(WORKFLOW_STORE, id);
  }

  async executeWorkflow(workflowId: string): Promise<StepResult[]> {
    const workflow = await this.getWorkflow(workflowId);
    if (!workflow) throw new Error('Workflow not found');

    const results: StepResult[] = [];
    for (const step of workflow.steps) {
      try {
        const result = await executeStep(step);
        results.push(result);
        await this.db.put(RESULT_STORE, result);
        this.syncQueue.push(result);
      } catch (e: any) {
        const result: StepResult = {
          stepId: step.id,
          status: 'failed',
          error: e.message,
        };
        results.push(result);
        await this.db.put(RESULT_STORE, result);
        this.syncQueue.push(result);
      }
    }
    return results;
  }

  /* ---------- Sync ---------- */
  async syncResultsWhenOnline(): Promise<void> {
    if (!navigator.onLine) return;

    // Simple batch sync – replace with your API client
    const payload = this.syncQueue;
    if (!payload.length) return;

    try {
      // await api.post('/sync', payload);
      console.log('Syncing', payload);
      this.syncQueue = []; // clear on success
    } catch (e) {
      console.warn('Sync failed, will retry later', e);
      // keep queue for next attempt
    }
  }

  /* ---------- Helpers ---------- */
  async listWorkflows(): Promise<Workflow[]> {
    return this.db.getAll(WORKFLOW_STORE);
  }
}

export const workflowEngine = new OfflineWorkflowEngine();