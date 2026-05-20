import { Resource } from '../types/resource';

// Configuration for idle detection (can be externalized later)
const IDLE_THRESHOLD_SECONDS = 1800; // 30 minutes

export class IdleDetector {
  /**
   * Checks if a resource is considered idle based on its last activity time.
   * @param resource The resource to check.
   * @returns True if the resource is idle, false otherwise.
   */
  isResourceIdle(resource: Resource): boolean {
    const now = Date.now();
    const timeSinceLastActivity = now - resource.last_activity;
    return timeSinceLastActivity > IDLE_THRESHOLD_SECONDS * 1000;
  }

  /**
   * Processes a list of resources and returns an array of idle resources.
   * @param resources The list of resources to check.
   * @returns An array of resources marked as idle.
   */
  detectIdleResources(resources: Resource[]): Resource[] {
    return resources.filter(this.isResourceIdle.bind(this));
  }

  /**
   * Updates the status of idle resources to 'idle' and logs them.
   * This can be extended to trigger notifications or shutdown actions.
   * @param idleResources The list of detected idle resources.
   */
  handleIdleResources(idleResources: Resource[]): void {
    console.log(`Detected ${idleResources.length} idle resources:`);
    idleResources.forEach(resource => {
      console.log(`  - Resource ID: ${resource.id}, Type: ${resource.type}`);
    });
    // In a real implementation, this would update the resource status
    // and potentially trigger a shutdown workflow.
  }
}

// Export the class for external use
export default IdleDetector;