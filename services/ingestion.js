/**
 * Stub for ingestion job enqueuing logic.
 *
 * Simulates a successful async enqueue operation.
 */

async function enqueueIngestionJob(taskId, data) {
  // Validate inputs exist before "sending"
  if (!taskId) {
    throw new Error('taskId is required for ingestion');
  }

  // Simulate async queue operation
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      console.log(`[Ingestion] Enqueued job for task: ${taskId}`);
      console.log(`[Ingestion] Payload data:`, data);
      resolve();
    }, 100);
  });
}

module.exports = { enqueueIngestionJob };