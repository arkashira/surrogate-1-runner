import * as crypto from 'crypto';

export class EncryptionService {
  private algorithm: string = 'aes-256-cbc';
  private key: Buffer;
  private iv: Buffer;

  constructor(key: string, iv: string) {
    this.key = Buffer.from(key, 'hex');
    this.iv = Buffer.from(iv, 'hex');
  }

  encrypt(data: string): string {
    const cipher = crypto.createCipher(this.algorithm, this.key, this.iv);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
  }

  decrypt(encrypted: string): string {
    const decipher = crypto.createDecipher(this.algorithm, this.key, this.iv);
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}