import { workflowEngine } from './services/workflowEngine';

(async () => {
  await workflowEngine.init();

  // Example usage
  const wf = {
    id: 'demo',
    name: 'Demo Workflow',
    steps: [{ id: 's1', type: 'http', config: {} }],
  };
  await workflowEngine.addWorkflow(wf);
  const results = await workflowEngine.executeWorkflow('demo');
  console.log('Workflow results:', results);

  // Auto‑sync when back online
  window.addEventListener('online', () => workflowEngine.syncResultsWhenOnline());
})();