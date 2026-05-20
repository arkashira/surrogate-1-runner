const request = require('supertest');
const app = require('../api/index');

describe('Feedback API', () => {
  it('should submit feedback successfully', async () => {
    const response = await request(app)
      .post('/api/feedback/submit')
      .send({
        issue: 'Test issue',
        suggestion: 'Test suggestion',
        rating: 5
      });

    expect(response.status).toBe(200);
    expect(response.text).toBe('Feedback submitted successfully.');
  });

  it('should return 400 if no fields are filled', async () => {
    const response = await request(app)
      .post('/api/feedback/submit')
      .send({});

    expect(response.status).toBe(400);
    expect(response.text).toBe('At least one field must be filled.');
  });
});