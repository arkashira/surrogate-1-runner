import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';

interface ShareLinkPayload {
  userId: string;
  dashboardId: string;
  expiresAt: number;
}

const SECRET_KEY = process.env.JWT_SECRET_KEY || 'default-secret-key';

export class ShareLinkService {
  private static generateToken(payload: ShareLinkPayload): string {
    return jwt.sign(payload, SECRET_KEY, { expiresIn: '24h' });
  }

  private static generatePayload(userId: string, dashboardId: string): ShareLinkPayload {
    const expiresAt = Date.now() + 24 * 60 * 60 * 1000; // 24 hours from now
    return {
      userId,
      dashboardId,
      expiresAt,
    };
  }

  public static async createShareLink(userId: string, dashboardId: string): Promise<string> {
    const payload = ShareLinkService.generatePayload(userId, dashboardId);
    const token = ShareLinkService.generateToken(payload);
    const shareLinkId = uuidv4();
    // Store the shareLinkId and token in a database or cache for validation later
    // For simplicity, we're just returning the token here
    return `${process.env.BASE_URL}/dashboard/${dashboardId}?token=${token}`;
  }

  public static async validateShareLink(token: string): Promise<ShareLinkPayload | null> {
    try {
      const decoded = jwt.verify(token, SECRET_KEY) as ShareLinkPayload;
      if (decoded.expiresAt < Date.now()) {
        return null;
      }
      return decoded;
    } catch (error) {
      console.error('Error validating share link:', error);
      return null;
    }
  }
}