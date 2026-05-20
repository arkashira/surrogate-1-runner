/**
 * Checks whether the incoming request contains the required
 * SAML attribute that grants access to the web‑shell UI.
 *
 * The attribute name is configurable via the environment variable
 * `WEB_SHELL_AUTH_ATTRIBUTE`.  If the variable is not set, the
 * default value is `urn:axentx:role:webshell`.
 *
 * The attribute value can be a single string or an array of strings.
 * Any of the following values are considered “true”:
 *   - 'true'
 *   - '1'
 *   - 'yes'
 *
 * @param {Object} req Express request object
 * @returns {boolean} true if the request is authorised, false otherwise
 */
const REQUIRED_ATTRIBUTE =
  process.env.WEB_SHELL_AUTH_ATTRIBUTE ||
  'urn:axentx:role:webshell';

function isAuthorized(req) {
  if (!req || !req.saml || !req.saml.attributes) {
    return false;
  }

  const attrs = req.saml.attributes;
  const raw = attrs[REQUIRED_ATTRIBUTE];

  if (raw === undefined || raw === null) {
    return false;
  }

  const values = Array.isArray(raw) ? raw : [raw];

  return values.some(v =>
    typeof v === 'string' &&
    ['true', '1', 'yes'].includes(v.toLowerCase())
  );
}

module.exports = { isAuthorized };