const request = require('supertest');
const app = require('../app'); // Assuming app is exported from app.js

describe('POST /invite', () => {
  it('should send invitations to up to 10 team members', async () => {
    const response = await request(app)
      .post('/invite')
      .send({ emails: ['test1@example.com', 'test2@example.com'] });

    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Invitations sent successfully');
  });

  it('should not allow inviting more than 10 team members', async () => {
    const response = await request(app)
      .post('/invite')
      .send({ emails: Array(11).fill('test@example.com') });

    expect(response.status).toBe(400);
    expect(response.body.message).toBe('Cannot invite more than 10 team members at once');
  });

  it('should handle invalid input', async () => {
    const response = await request(app)
      .post('/invite')
      .send({});

    expect(response.status).toBe(400);
    expect(response.body.message).toBe('No emails provided');
  });
});