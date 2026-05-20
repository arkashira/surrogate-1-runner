const { isAuthorized } = require('../auth');

describe('isAuthorized', () => {
  const baseReq = {
    saml: {
      attributes: {},
    },
  };

  test('rejects when no req.saml', () => {
    expect(isAuthorized({})).toBe(false);
  });

  test('rejects when attribute missing', () => {
    expect(isAuthorized(baseReq)).toBe(false);
  });

  test('accepts single true value', () => {
    const req = {
      saml: { attributes: { 'urn:axentx:role:webshell': 'true' } },
    };
    expect(isAuthorized(req)).toBe(true);
  });

  test('accepts array of values', () => {
    const req = {
      saml: {
        attributes: {
          'urn:axentx:role:webshell': ['no', 'yes', 'maybe'],
        },
      },
    };
    expect(isAuthorized(req)).toBe(true);
  });

  test('rejects false values', () => {
    const req = {
      saml: { attributes: { 'urn:axentx:role:webshell': 'false' } },
    };
    expect(isAuthorized(req)).toBe(false);
  });
});