const request = require('supertest');
const express = require('express');
const summaryRouter = require('../../dashboard/summary');

describe('Dashboard Summary API', () => {
  let app;

  beforeAll(() => {
    app = express();
    // Mount the router at the expected path
    app.use('/dashboard/summary', summaryRouter);
  });

  test('GET /dashboard/summary returns expected structure', async () => {
    const response = await request(app).get('/dashboard/summary');
    expect(response.status).toBe(200);
    const data = response.body;

    // Verify totalMonthlyCost exists and is a number
    expect(typeof data.totalMonthlyCost).toBe('number');

    // Verify topCategories is an array of length 5 with required fields
    expect(Array.isArray(data.topCategories)).toBe(true);
    expect(data.topCategories).toHaveLength(5);
    data.topCategories.forEach((cat) => {
      expect(typeof cat.category).toBe('string');
      expect(typeof cat.cost).toBe('number');
    });

    // Verify costTrend is an array with month & cost fields
    expect(Array.isArray(data.costTrend)).toBe(true);
    data.costTrend.forEach((point) => {
      expect(typeof point.month).toBe('string');
      expect(typeof point.cost).toBe('number');
    });
  });
});