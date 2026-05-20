import { v4 as uuidv4 } from 'uuid';

/**
 * Represents a shell session.
 */
export interface ShellSession {
  id: string;
  user: string;
  node: string;
  startTime: Date;
  status: 'active' | 'terminated';
}

/**
 * In-memory store for active sessions.
 * In a real implementation this would be backed by a database or
 * a distributed session store.
 */
const sessionStore: Map<string, ShellSession> = new Map();

/**
 * Create a new shell session (used by other parts of the system).
 * This helper is not part of the requested feature but is useful
 * for testing and demonstration purposes.
 */
export function createSession(user: string, node: string): ShellSession {
  const session: ShellSession = {
    id: uuidv4(),
    user,
    node,
    startTime: new Date(),
    status: 'active',
  };
  sessionStore.set(session.id, session);
  return session;
}

/**
 * Retrieve all active sessions.
 */
export async function getActiveSessions(): Promise<ShellSession[]> {
  // In a real system this might involve async DB calls.
  return Array.from(sessionStore.values()).filter(
    (s) => s.status === 'active'
  );
}

/**
 * Terminate a session by ID.
 * @throws {Error} if the session does not exist or is already terminated.
 */
export async function terminateSession(sessionId: string): Promise<void> {
  const session = sessionStore.get(sessionId);
  if (!session) {
    const err = new Error('SessionNotFound');
    throw err;
  }
  if (session.status === 'terminated') {
    const err = new Error('SessionAlreadyTerminated');
    throw err;
  }
  // Mark as terminated and remove from store
  session.status = 'terminated';
  sessionStore.delete(sessionId);
}