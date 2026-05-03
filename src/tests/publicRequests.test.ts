import request from 'supertest';
import app from '../app';

describe('GET /public/requests/:publicId', () => {
  it('should return 200 and the request details', async () => {
    const publicId = 'example-public-id';
    const requestService = new RequestService();
    const request = await requestService.getRequestByPublicId(publicId);
    const response = await request(app).get(`/public/requests/${publicId}`);
    expect(response.status).toBe(200);
    expect(response.body).toEqual({
      title: request.title,
      status: request.status,
      timeline: request.timeline,
      sla: request.sla,
      lastUpdated: request.lastUpdated,
      statusLabel: getRequestStatusLabel(request.status),
    });
  });

  it('should return 404 for unknown publicId', async () => {
    const publicId = 'unknown-public-id';
    const response = await request(app).get(`/public/requests/${publicId}`);
    expect(response.status).toBe(404);
    expect(response.text).toBe('Request not found');
  });
});