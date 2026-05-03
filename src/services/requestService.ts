import { notifyQueue, StatusChangePayload } from '../queue/notifyQueue';

const PUBLIC_BASE = process.env.PUBLIC_BASE_URL || 'https://app.axentx.io';

/**
 * Enqueue a notification for a request status change.
 * Call this in your request update flow after persisting the new status.
 */
export async function notifyOnStatusChange(
  requestId: string,
  oldStatus: string,
  newStatus: string
): Promise<void> {
  const publicUrl = `${PUBLIC_BASE}/requests/${requestId}`;

  const payload: StatusChangePayload = {
    requestId,
    oldStatus,
    newStatus,
    publicUrl,
  };

  await notifyQueue.add('status-change', payload);
}