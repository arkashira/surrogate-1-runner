const request = require('supertest');
const express = require('express');
const validateKeyRouter = require('../../src/api/validateKey');

const app = express();
app.use(express.json());
app.use('/validate-key', validateKeyRouter);

describe('POST /validate-key', () => {
  test('returns valid true for a correctly formatted key', async () => {
    const res = await request(app)
      .post('/validate-key')
      .send({ apiKey: 'A1B2C3D4E5F6G7H8I9J0K1L2' });
    expect(res.statusCode).toBe(200);
    expect(res.body).toEqual({ valid: true });
  });

  test('rejects a key that is too short', async () => {
    const res = await request(app)
      .post('/validate-key')
      .send({ apiKey: 'short-key' });
    expect(res.statusCode).toBe(400);
    expect(res.body.valid).toBe(false);
    expect(res.body.error).toBe('Invalid API key format');
  });

  test('rejects when apiKey is missing', async () => {
    const res = await request(app)
      .post('/validate-key')
      .send({});
    expect(res.statusCode).toBe(400);
    expect(res.body.valid).toBe(false);
    expect(res.body.error).toBe('apiKey must be a string');
  });
});