const request = require('supertest');
const app = require('../interface');

// Helper to build a request with a SAML assertion
const samlReq = (attrs) => ({
  saml: { attributes: attrs, nameID: 'test-user' },
});

describe('Web shell access control', () => {
  test('allows authorised user', async () => {
    const res = await request(app)
      .get('/api/status')
      .set('X-Request-Id', 'dummy') // any header to trigger the request
      .use((req) => {
        // inject our fake SAML object
        req.saml = samlReq({
          'urn:axentx:role:webshell': 'true',
        });
      });

    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.body.user).toBe('test-user');
  });

  test('denies unauthorised user', async () => {
    const res = await request(app)
      .get('/api/status')
      .use((req) => {
        req.saml = samlReq({
          'urn:axentx:role:webshell': 'false',
        });
      });

    expect(res.status).toBe(403);
    expect(res.text).toContain('Forbidden');
  });
});