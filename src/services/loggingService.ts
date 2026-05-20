export interface SessionLog {
  /** Username of the person attempting the session */
  user: string;
  /** Target node hostname */
  node: string;
  /** Role of the user */
  role: string;
  /** ISO timestamp of the attempt */
  timestamp: string;
  /** Whether the session was successfully started */
  success: boolean;
  /** Optional error message if the attempt failed */
  error?: string;
}

/**
 * Persist a shell session attempt.
 *
 * In a real deployment this would write to a database or external
 * logging service. For the purposes of this repository we simply
 * output a JSON string to stdout so that the logs are captured
 * by the CI environment.
 */
export function logSessionAttempt(log: SessionLog): void {
  const logEntry = {
    user: log.user,
    node: log.node,
    role: log.role,
    timestamp: log.timestamp,
    success: log.success,
    ...(log.error ? { error: log.error } : {}),
  };
  console.log(JSON.stringify(logEntry));
}