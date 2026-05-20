import { ShareLinkService } from '../shareLink';
import jwt from 'jsonwebtoken';

describe('ShareLinkService', () => {
  const userId = 'test-user-id';
  const dashboardId = 'test-dashboard-id';
  const secretKey = 'test-secret-key';

  beforeAll(() => {
    process.env.JWT_SECRET_KEY = secretKey;
  });

  afterAll(() => {
    delete process.env.JWT_SECRET_KEY;
  });

  it('should create a valid share link', async () => {
    const shareLink = await ShareLinkService.createShareLink(userId, dashboardId);
    expect(shareLink).toContain(`dashboard/${dashboardId}`);
    expect(shareLink).toContain('?token=');

    const token = shareLink.split('?token=')[1];
    const decoded = jwt.verify(token, secretKey) as ShareLinkPayload;
    expect(decoded.userId).toBe(userId);
    expect(decoded.dashboardId).toBe(dashboardId);
    expect(decoded.expiresAt).toBeGreaterThan(Date.now());
  });

  it('should validate a valid share link', async () => {
    const shareLink = await ShareLinkService.createShareLink(userId, dashboardId);
    const token = shareLink.split('?token=')[1];
    const decoded = await ShareLinkService.validateShareLink(token);
    expect(decoded?.userId).toBe(userId);
    expect(decoded?.dashboardId).toBe(dashboardId);
    expect(decoded?.expiresAt).toBeGreaterThan(Date.now());
  });

  it('should not validate an expired share link', async () => {
    const payload = ShareLinkService.generatePayload(userId, dashboardId);
    payload.expiresAt = Date.now() - 1000; // Expired 1 second ago
    const token = ShareLinkService.generateToken(payload);
    const decoded = await ShareLinkService.validateShareLink(token);
    expect(decoded).toBeNull();
  });
});