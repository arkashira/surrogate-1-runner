// ------------------------------------------------------------
// src/scheduler.ts   (merge snippet)
// ------------------------------------------------------------
import { scheduleJob } from 'node-schedule';
import { cleanupIssueEvents } from './jobs/cleanupIssueEvents';

// -------------------------------------------------------------------
// Helper: schedule a daily midnight job that runs the cleanup task.
// -------------------------------------------------------------------
export function scheduleRetentionCleanup(): void {
  // Cron expression: “0 0 * * *” → every day at 00:00 (midnight) UTC.
  // If you need local time, adjust the expression or use a timezone option.
  scheduleJob('0 0 * * *', async () => {
    try {
      await cleanupIssueEvents();
    } catch (e) {
      // The cleanup function already logs; we just prevent the scheduler
      // from crashing the whole process.
      console.error('[scheduleRetentionCleanup] Unexpected error', e);
    }
  });
}

// -------------------------------------------------------------------
// If your file already exports a function that registers all jobs,
// add a call to the new scheduler there, e.g.:
//
// export function registerAllJobs() {
//   scheduleSomethingElse();
//   scheduleRetentionCleanup();   // <-- add this line
// }
// -------------------------------------------------------------------