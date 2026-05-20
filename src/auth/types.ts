export interface RecoveryEntry {
  userId: string;
  codeHash: string;          // SHA‑256 hash of the plain code
  expiresAt: Date;           // When the code becomes invalid
  used: boolean;             // Has the code already been consumed?
  createdAt: Date;
}

export interface AuditLogger {
  log(event: string, payload: Record<string, unknown>): void;
}