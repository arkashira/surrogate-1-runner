export type ProviderType = 'openai' | 'anthropic' | 'google' | 'azure' | 'ollama' | 'huggingface';

export interface ProviderConfig {
  id: string;
  type: ProviderType;
  name: string;
  apiKey: string;
  baseUrl?: string;
  enabled: boolean;
  createdAt: Date;
  lastUsed?: Date;
}

export interface CredentialEntry {
  providerId: string;
  providerType: ProviderType;
  encryptedKey: string;
  keyVersion: number;
  encryptedAt: Date;
  expiresAt?: Date;
}

export interface StorageResult {
  success: boolean;
  error?: string;
  data?: ProviderConfig | CredentialEntry;
}