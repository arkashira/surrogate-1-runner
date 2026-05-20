import request from 'supertest';
import app from './app';
import policyService from './policy-service';

describe('Policies API', () => {
  it('should create a new policy', async () => {
    const policy = {
      name: 'Test Policy',
      maxInstanceSize: 'small',
      idleTimeout: '30m',
    };

    const response = await request(app)
      .post('/api/policies')
      .send(policy);

    expect(response.status).toBe(201);
    expect(response.body.name).toBe(policy.name);
  });
});