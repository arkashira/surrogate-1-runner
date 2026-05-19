// ------------------------------------------------------------
// src/jobs/cleanupIssueEvents.ts
// ------------------------------------------------------------
import { db } from '../db';
import { IssueEvent } from '../models/IssueEvent';
import { Op } from 'sequelize';
import logger from '../logger';   // <-- adjust path if you have a logger util

/**
 * Number of days to keep IssueEvent rows.
 * Make this configurable via env if you need flexibility.
 */
const RETENTION_DAYS = Number(process.env.ISSUE_EVENT_RETENTION_DAYS ?? 90);

/**
 * Delete IssueEvent records older than RETENTION_DAYS.
 * Returns the number of rows removed (useful for monitoring).
 */
export async function cleanupIssueEvents(): Promise<number> {
  const cutoff = new Date(Date.now() - RETENTION_DAYS * 24 * 60 * 60 * 1000);

  try {
    const deleted = await db.IssueEvent.destroy({
      where: {
        createdAt: {
          [Op.lt]: cutoff,
        },
      },
    });

    logger.info(
      `[cleanupIssueEvents] Deleted ${deleted} IssueEvent rows older than ${cutoff.toISOString()}`
    );
    return deleted;
  } catch (err) {
    logger.error('[cleanupIssueEvents] Failed to clean up IssueEvents', err);
    throw err; // let the scheduler surface the failure
  }
}