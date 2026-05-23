import { Workflow } from './types/workflow';
import * as LocalForage from 'localforage';

class WorkflowStorage {
  private db: LocalForage;

  constructor() {
    this.db = LocalForage.createInstance({
      name: 'workflows',
    });
  }

  async saveWorkflow(workflow: Workflow): Promise<void> {
    await this.db.set(workflow.id, workflow);
  }

  async getWorkflow(id: string): Promise<Workflow | null> {
    return await this.db.get(id);
  }

  async deleteWorkflow(id: string): Promise<void> {
    await this.db.removeItem(id);
  }

  async getAllWorkflows(): Promise<Workflow[]> {
    const keys = await this.db.keys();
    const workflows: Workflow[] = await Promise.all(keys.map((key) => this.db.get(key)));
    return workflows;
  }
}

export default new WorkflowStorage();