import { RecoveryRepository, RecoveryEntry } from "./types";

export class InMemoryRecoveryRepository implements RecoveryRepository {
  private store = new Map<string, RecoveryEntry[]>(); // key = userId

  async add(entry: RecoveryEntry): Promise<void> {
    const list = this.store.get(entry.userId) ?? [];
    list.push(entry);
    this.store.set(entry.userId, list);
  }

  async findValid(userId: string, codeHash: string, now: Date): Promise<RecoveryEntry | undefined> {
    const list = this.store.get(userId) ?? [];
    return list.find(
      (e) => !e.used && e.codeHash === codeHash && e.expiresAt > now
    );
  }

  async markUsed(entry: RecoveryEntry): Promise<void> {
    entry.used = true;
  }

  async list(userId: string): Promise<RecoveryEntry[]> {
    return this.store.get(userId) ?? [];
  }

  async deleteExpired(now: Date): Promise<number> {
    let deleted = 0;
    for (const [userId, list] of this.store.entries()) {
      const remaining = list.filter((e) => e.expiresAt > now);
      deleted += list.length - remaining.length;
      this.store.set(userId, remaining);
    }
    return deleted;
  }
}