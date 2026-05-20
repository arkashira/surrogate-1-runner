import * as crypto from 'crypto';
import * as fs from 'fs';
import * as path from 'path';
import { CredentialEntry, ProviderConfig, ProviderType, StorageResult } from '../types/providers';

const ENCRYPTION_KEY = process.env.SECURE_STORAGE_KEY || crypto.randomBytes(32).toString('hex');
const ENCRYPTION_IV_SIZE = 16;
const CREDENTIALS_PATH = path.join(process.env.AXENTX_DATA_DIR || '/opt/axentx/surrogate-1', 'credentials.json');

const ALGORITHM = 'aes-256-gcm';

function generateIV(): Buffer {
  return crypto.randomBytes(ENCRYPTION_IV_SIZE);
}

function encrypt(data: string): string {
  const iv = generateIV();
  const key = Buffer.from(ENCRYPTION_KEY, 'hex');
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  return iv.toString('hex') + ':' + authTag.toString('hex') + ':' + encrypted;
}

function decrypt(encryptedData: string): string {
  const parts = encryptedData.split(':');
  if (parts.length !== 3) {
    throw new Error('Invalid encrypted data format');
  }
  const iv = Buffer.from(parts[0], 'hex');
  const authTag = Buffer.from(parts[1], 'hex');
  const encrypted = parts[2];
  const key = Buffer.from(ENCRYPTION_KEY, 'hex');
  const decipher = crypto.createDecipheriv(ALGORITHM, key, iv);
  decipher.setAuthTag(authTag);
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

function loadCredentials(): Map<string, CredentialEntry> {
  try {
    if (!fs.existsSync(CREDENTIALS_PATH)) {
      return new Map();
    }
    const data = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
    const credentials = new Map<string, CredentialEntry>();
    for (const [id, entry] of Object.entries(data)) {
      credentials.set(id, entry as CredentialEntry);
    }
    return credentials;
  } catch (error) {
    console.error('Failed to load credentials:', error);
    return new Map();
  }
}

function saveCredentials(credentials: Map<string, CredentialEntry>): void {
  try {
    const data: Record<string, CredentialEntry> = {};
    for (const [id, entry] of credentials) {
      data[id] = entry;
    }
    fs.writeFileSync(CREDENTIALS_PATH, JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Failed to save credentials:', error);
    throw new Error('Failed to persist credentials');
  }
}

export class SecureCredentialStore {
  private credentials: Map<string, CredentialEntry>;

  constructor() {
    this.credentials = loadCredentials();
  }

  async store(providerId: string, providerType: ProviderType, apiKey: string): Promise<StorageResult> {
    try {
      const encryptedKey = encrypt(apiKey);
      const entry: CredentialEntry = {
        providerId,
        providerType,
        encryptedKey,
        keyVersion: 1,
        encryptedAt: new Date(),
      };
      this.credentials.set(providerId, entry);
      saveCredentials(this.credentials);
      return { success: true, data: entry };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  async retrieve(providerId: string): Promise<StorageResult> {
    try {
      const entry = this.credentials.get(providerId);
      if (!entry) {
        return { success: false, error: 'Provider credential not found' };
      }
      const apiKey = decrypt(entry.encryptedKey);
      return { success: true, data: { providerId, providerType: entry.providerType, apiKey } };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  async remove(providerId: string): Promise<StorageResult> {
    try {
      if (this.credentials.has(providerId)) {
        this.credentials.delete(providerId);
        saveCredentials(this.credentials);
        return { success: true };
      }
      return { success: false, error: 'Provider credential not found' };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  async list(): Promise<StorageResult> {
    try {
      const entries: Array<{ providerId: string; providerType: ProviderType }> = [];
      for (const [id, entry] of this.credentials) {
        entries.push({ providerId: id, providerType: entry.providerType });
      }
      return { success: true, data: entries };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  async update(providerId: string, providerType: ProviderType, apiKey: string): Promise<StorageResult> {
    try {
      const encryptedKey = encrypt(apiKey);
      const entry: CredentialEntry = {
        providerId,
        providerType,
        encryptedKey,
        keyVersion: 2,
        encryptedAt: new Date(),
      };
      this.credentials.set(providerId, entry);
      saveCredentials(this.credentials);
      return { success: true, data: entry };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }
}

export const secureStore = new SecureCredentialStore();