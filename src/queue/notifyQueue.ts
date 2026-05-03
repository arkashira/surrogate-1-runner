import { Queue, Worker, Job } from 'bullmq';
import IORedis from 'ioredis';

const redisOpts = process.env.REDIS_URL
  ? { connection: { url: process.env.REDIS_URL } }
  : // memory fallback for local/dev — remove in prod if undesired
    ({ useSharedConnections: false, useDelayedStreams: false } as any);

const connection = process.env.REDIS_URL
  ? new IORedis(process.env.REDIS_URL)
  : // BullMQ will use an in-memory connection when `connection` is undefined
    undefined;

export const notifyQueue = new Queue('status-notify', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: 100,
    removeOnFail: 50,
  },
});

export interface StatusChangePayload {
  requestId: string;
  oldStatus: string;
  newStatus: string;
  publicUrl: string;
}

// Graceful shutdown helper
export async function closeNotifyQueue(): Promise<void> {
  await notifyQueue.close();
}