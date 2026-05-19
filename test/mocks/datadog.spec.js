const request = require('supertest');
const express = require('express');
const metricsRouter = require('../../src/endpoints/datadog/metrics');

describe('Mock Datadog /api/v2/metrics endpoint', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json()); // parse JSON bodies
    app.use(metricsRouter);
  });

  test('responds 200 with correct JSON structure on valid request', async () => {
    const payload = {
      metric: 'test.metric',
      tags: ['env:test'],
      host: 'unit-test',
      interval: 30
    };

    const response = await request(app)
      .post('/api/v2/metrics')
      .set('DD-API-KEY', 'dummy-key')
      .set('Content-Type', 'application/json')
      .send(payload)
      .expect(200);

    // Verify response shape
    expect(response.body).toHaveProperty('data');
    expect(Array.isArray(response.body.data)).toBe(true);
    const series = response.body.data[0];
    expect(series).toMatchObject({
      type: 'metric_series',
      attributes: {
        metric: 'test.metric',
        tags: [],
        host: 'mock-host',
        interval: 60
      }
    });
    expect(Array.isArray(series.attributes.points)).toBe(true);
    expect(series.attributes.points[0].length).toBe(2);
    expect(typeof series.attributes.points[0][0]).toBe('number'); // timestamp
    expect(typeof series.attributes.points[0][1]).toBe('number'); // value
  });

  test('rejects request without API key', async () => {
    const response = await request(app)
      .post('/api/v2/metrics')
      .set('Content-Type', 'application/json')
      .send({});

    expect(response.status).toBe(403);
    expect(response.body).toHaveProperty('errors');
  });

  test('rejects request with wrong content type', async () => {
    const response = await request(app)
      .post('/api/v2/metrics')
      .set('DD-API-KEY', 'dummy')
      .set('Content-Type', 'text/plain')
      .send('not json');

    expect(response.status).toBe(415);
    expect(response.body).toHaveProperty('errors');
  });

  test('rejects request with invalid JSON payload', async () => {
    const response = await request(app)
      .post('/api/v2/metrics')
      .set('DD-API-KEY', 'dummy-key')
      .set('Content-Type', 'application/json')
      .send('not json');

    expect(response.status).toBe(400);
    expect(response.body).toHaveProperty('errors');
  });
});