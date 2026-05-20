import { detectIdleResources } from './services/resource-monitor';
import { executeShutdownAction } from './services/action-executor';
import { notifyUser } from './services/notification-service';

async function shutdownActionWorkflow() {
  try {
    const idleResources = await detectIdleResources();
    console.log(`Detected ${idleResources.length} idle resources.`);

    // Flagging resources for shutdown
    const flaggedResources = idleResources.map(resource => ({
      ...resource,
      status: 'flagged_for_shutdown'
    }));

    // Simulate policy approval process
    const approvedResources = flaggedResources.filter(() => Math.random() > 0.5);
    console.log(`Approved ${approvedResources.length} resources for shutdown.`);

    // Execute shutdown actions
    for (const resource of approvedResources) {
      await executeShutdownAction(resource);
      console.log(`Shutdown action executed for resource: ${resource.id}`);
    }

    // Notify users about the actions taken
    await notifyUser(approvedResources);
    console.log('Notifications sent to users.');

  } catch (error) {
    console.error('Error in shutdown action workflow:', error);
  }
}

shutdownActionWorkflow();