const request = require('supertest');
const app = require('../app');
const analyticsPipeline = require('../analytics/pipeline');

describe('Specs route', () => {
  it('should create a spec and emit an event', async () => {
    jest.spyOn(analyticsPipeline, 'emitEvent');

    const response = await request(app)
      .post('/specs/create')
      .send({ templateType: 'test-template' })
      .set('Authorization', 'Bearer test-token');

    expect(response.status).toBe(201);
    expect(analyticsPipeline.emitEvent).toHaveBeenCalledWith('spec.created', {
      userId: 'test-user-id',
      timestamp: expect.any(String),
      templateType: 'test-template',
    });
  });
});