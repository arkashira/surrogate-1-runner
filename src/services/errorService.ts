// healthRoute.test.js
import request from 'supertest';
import app from '../src/api/app'; // Express app

describe('GET /health', () => {
  test('returns 200 and JSON body', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.headers['content-type']).toMatch(/json/);
    expect(res.body).toHaveProperty('parsers');
  });

  test('each parser has healthy, memoryUsage, and optional crashLog', async () => {
    const res = await request(app).get('/health');
    const parsers = res.body.parsers;
    parsers.forEach(p => {
      expect(p).toHaveProperty('healthy');
      expect(typeof p.healthy).toBe('boolean');
      expect(p).toHaveProperty('memoryUsage');
      expect(typeof p.memoryUsage).toBe('number');
      if (p.crashLog !== undefined) {
        expect(typeof p.crashLog).toBe('string');
      }
    });
  });

  test('returns 500 on internal error', async () => {
    // Simulate internal error by mocking ParserManager
    jest.spyOn(ParserManager.prototype, 'getParserHealth').mockImplementation(() => {
      throw new Error('boom');
    });
    const res = await request(app).get('/health');
    expect(res.status).toBe(500);
    expect(res.body).toHaveProperty('error', 'boom');
  });
});