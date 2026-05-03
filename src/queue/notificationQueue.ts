import Redis from 'ioredis';
import { NotificationJob } from '../types/notification';
import { config } from '../config';

const redis = process.env.REDIS_URL
  ? new Redis(process.env.REDIS_URL)
  : new Redis({ enableOfflineQueue: false });

const QUEUE_KEY = 'notifications:pending';
const PROCESSING_KEY = 'notifications:processing';
const RATE_LIMIT_PREFIX = 'notifications:rl:';

function rateLimitKey(requestId: string) {
  return `${RATE_LIMIT_PREFIX}${requestId}`;
}

export async function enqueueNotification(job: NotificationJob): Promise<boolean> {
  const rlKey = rateLimitKey(job.requestId);
  const exists = await redis.get(rlKey);
  if (exists) return false;

  const ttlSec = Math.ceil(config.rateLimitWindowMs / 1000);
  const multi = redis.multi();
  multi.setex(rlKey, ttlSec, '1');
  multi.rpush(QUEUE_KEY, JSON.stringify({ ...job, timestamp: job.timestamp || Date.now() }));
  await multi.exec();
  return true;
}

export async function dequeueNotification(timeoutSec = 5): Promise<NotificationJob | null> {
  const result = await redis.brpoplpush(QUEUE_KEY, PROCESSING_KEY, timeoutSec);
  if (!result) return null;
  try {
    return JSON.parse(result) as NotificationJob;
  } catch {
    await redis.lrem(PROCESSING_KEY, 1, result);
    return null;
  }
}

export async function acknowledgeJob(job: NotificationJob): Promise<void> {
  await redis.lrem(PROCESSING_KEY, 1, JSON.stringify(job));
}

export async function requeueJob(job: NotificationJob): Promise<void
