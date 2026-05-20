export interface IDataStore {
  save(key: string, value: unknown): Promise<void>;
  get<T>(key: string): Promise<T | undefined>;
  delete(key: string): Promise<boolean>;
}

export class DataStore implements IDataStore {
  private store: Map<string, unknown>;

  constructor() {
    this.store = new Map();
  }

  async save(key: string, value: unknown): Promise<void> {
    if (!key || typeof key !== 'string') {
      throw new Error('Invalid key: must be a non-empty string');
    }
    if (value === undefined) {
      throw new Error('Invalid value: cannot be undefined');
    }
    this.store.set(key, { value, timestamp: Date.now() });
  }

  async get<T>(key: string): Promise<T | undefined> {
    const entry = this.store.get(key) as { value: T; timestamp: number } | undefined;
    return entry?.value;
  }

  async delete(key: string): Promise<boolean> {
    return this.store.delete(key);
  }

  async clear(): Promise<void> {
    this.store.clear();
  }
}