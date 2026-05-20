import { RecoveryEntry } from "./types";

export interface RecoveryRepository {
  /** Persist a new recovery entry */
  add(entry: RecoveryEntry): Promise<void>;

  /** Find a single *valid* entry for a user and code hash */
  findValid(userId: string, codeHash: string, now: Date): Promise<RecoveryEntry | undefined>;

  /** Mark an entry as used */
  markUsed(entry: RecoveryEntry): Promise<void>;

  /** List all entries for a user (used for audit UIs) */
  list(userId: string): Promise<RecoveryEntry[]>;

  /** Optional housekeeping: delete all expired entries */
  deleteExpired(now: Date): Promise<number>;
}