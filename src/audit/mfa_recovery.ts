import { Logger } from '../utils/logger';
import { Database } from '../db';
import { UserId, RecoveryEvent } from '../types';
import { v4 as uuidv4 } from 'uuid';

/**
 * Audit trail for MFA recovery events.
 *
 * Each recovery event is persisted with a unique ID, user reference,
 * timestamp, method used, and a flag indicating whether the recovery
 * was successful. The audit records are stored in a dedicated
 * `mfa_recovery_audit` table.
 *
 * This module provides a simple API to log events, query them, and count successful recoveries.
 */

const logger = Logger.get('audit/mfa_recovery');

export interface MFARecoveryAuditEntry {
  id: string;
  userId: UserId;
  method: string;
  successful: boolean;
  createdAt: Date;
}

/**
 * Details recorded for an MFA recovery event.
 */
export interface MfaRecoveryDetails {
  /** The method used for recovery (e.g., "backup_codes", "email_link"). */
  method: string;
  /** IP address from which the recovery was initiated. */
  ipAddress: string;
  /** Optional user‑agent string for additional context. */
  userAgent?: string;
}

/**
 * Log an MFA recovery event.
 *
 * @param userId - The ID of the user performing the recovery.
 * @param details - Contextual information about the recovery attempt.
 * @returns The created audit entry.
 */
export async function recordMfaRecovery(
  userId: UserId,
  details: MfaRecoveryDetails
): Promise<MFARecoveryAuditEntry> {
  const id = uuidv4();
  const createdAt = new Date();
  const method = details.method;
  const successful = true; // Assuming recovery was successful for now.

  const query = `
    INSERT INTO mfa_recovery_audit (id, user_id, method, successful, created_at, ip_address, user_agent)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING id, user_id, method, successful, created_at
  `;

  try {
    const result = await Database.query<MFARecoveryAuditEntry>(query, [
      id,
      userId,
      method,
      successful,
      createdAt,
      details.ipAddress,
      details.userAgent,
    ]);

    const entry = result.rows[0];
    logger.info('Logged MFA recovery event', { entry });
    return entry;
  } catch (err) {
    logger.error('Failed to log MFA recovery event', { error: err, userId, method, details });
    throw err;
  }
}

/**
 * Retrieve audit entries for a specific user.
 *
 * @param userId - The ID of the user.
 * @returns Array of audit entries sorted by most recent first.
 */
export async function getRecoveryAuditForUser(userId: UserId): Promise<MFARecoveryAuditEntry[]> {
  const query = `
    SELECT id, user_id, method, successful, created_at, ip_address, user_agent
    FROM mfa_recovery_audit
    WHERE user_id = $1
    ORDER BY created_at DESC
  `;

  try {
    const result = await Database.query<MFARecoveryAuditEntry>(query, [userId]);
    return result.rows;
  } catch (err) {
    logger.error('Failed to retrieve MFA recovery audit', { error: err, userId });
    throw err;
  }
}

/**
 * Count the number of successful recoveries for a user.
 *
 * @param userId - The ID of the user.
 * @returns Number of successful recoveries.
 */
export async function countSuccessfulRecoveries(userId: UserId): Promise<number> {
  const query = `
    SELECT COUNT(*) AS count
    FROM mfa_recovery_audit
    WHERE user_id = $1 AND successful = TRUE
  `;

  try {
    const result = await Database.query<{ count: string }>(query, [userId]);
    return parseInt(result.rows[0].count, 10);
  } catch (err) {
    logger.error('Failed to count successful MFA recoveries', { error: err, userId });
    throw err;
  }
}