/**
 * Tests for the zero-code setup API.
 *
 * Uses Jest and Supertest to validate the endpoint.
 */

const request = require('supertest');
const express = require('express');
const mongoose = require('mongoose');
const zeroCodeSetupRouter = require('../../src/api/zeroCodeSetup');
const Tool = require('../../src/models/tool');

const app = express();
app.use(express.json());
app.use('/api/zero-code-setup', zeroCodeSetupRouter);

beforeAll(async () => {
  const mongoUri = 'mongodb://127.0.0.1:27017/axentx_test';
  await mongoose.connect(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true });
});

afterAll(async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.disconnect();
});

beforeEach(async () => {
  await Tool.deleteMany({});
});

describe('POST /api/zero-code-setup', () => {
  it('creates a new tool with minimal input', async () => {
    const res = await request(app)
      .post('/')
      .send({ name: 'MyTool' })
      .expect(201);

    expect(res.body).toHaveProperty('id');
    expect(res.body.name).toBe('MyTool');
    expect(res.body.description).toBe('');
    expect(res.body.config).toEqual({});
  });

  it('returns 400 if name is missing', async () => {
    const res = await request(app)
      .post('/')
      .send({ description: 'desc' })
      .expect(400);

    expect(res.body).toHaveProperty('error');
  });

  it('returns 409 if duplicate name', async () => {
    await Tool.create({ name: 'DuplicateTool' });

    const res = await request(app)
      .post('/')
      .send({ name: 'DuplicateTool' })
      .expect(409);

    expect(res.body).toHaveProperty('error');
  });
});