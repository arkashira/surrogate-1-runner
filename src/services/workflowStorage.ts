import { EncryptionService } from './encryptionService';

export class WorkflowStorage {
  private encryptionService: EncryptionService;
  private storage: Storage;

  constructor(key: string, iv: string) {
    this.encryptionService = new EncryptionService(key, iv);
    this.storage = localStorage;
  }

  saveWorkflow(workflow: string): void {
    const encryptedWorkflow = this.encryptionService.encrypt(workflow);
    this.storage.setItem('workflow', encryptedWorkflow);
  }

  getWorkflow(): string {
    const encryptedWorkflow = this.storage.getItem('workflow');
    if (encryptedWorkflow) {
      return this.encryptionService.decrypt(encryptedWorkflow);
    }
    return '';
  }
}