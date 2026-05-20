const fs = require('fs');
const path = require('path');
const xml2js = require('xml2js');
const { DOMParser } = require('xmldom');
const { SignedXml } = require('xml-crypto');
const pino = require('pino');
const logger = pino({ level: process.env.LOG_LEVEL || 'info' });

const { idpCertPath } = require('./config');
const idpCert = fs.readFileSync(idpCertPath, 'utf-8');

/**
 * Express middleware that:
 *   1. Reads `req.body.SAMLResponse`
 *   2. Base64‑decodes & parses the XML
 *   3. Validates the XML signature
 *   4. Normalises attributes into `req.saml`
 *   5. Stores the assertion in `req.session.saml`
 *
 * Errors are logged and a 400/500 response is sent.
 */
async function parseSAML(req, res, next) {
  try {
    const samlBase64 = req.body?.SAMLResponse;
    if (!samlBase64) {
      logger.warn('Missing SAMLResponse in POST body');
      return res.status(400).send('Bad Request: Missing SAMLResponse');
    }

    const samlXml = Buffer.from(samlBase64, 'base64').toString('utf-8');

    /* ---------- 1️⃣  Signature validation ---------- */
    const doc = new DOMParser().parseFromString(samlXml);
    const signatureNode = doc.getElementsByTagName('Signature')[0];
    if (!signatureNode) {
      logger.warn('No Signature element found in SAML Response');
      return res.status(400).send('Bad Request: Missing Signature');
    }

    const sig = new SignedXml();
    sig.keyInfoProvider = { getKeyInfo: () => '<X509Data></X509Data>' };
    sig.loadSignature(signatureNode);

    if (!sig.checkSignature(samlXml, { publiccert: idpCert })) {
      logger.warn('SAML signature validation failed', {
        errors: sig.validationErrors,
      });
      return res.status(400).send('Bad Request: Invalid SAML signature');
    }

    /* ---------- 2️⃣  XML → JS ---------- */
    const parser = new xml2js.Parser({ explicitArray: false, mergeAttrs: true });
    const parsed = await parser.parseStringPromise(samlXml);

    // Navigate to the AttributeStatement
    const assertion =
      parsed.Response?.Assertion ||
      parsed.Response?.['saml:Assertion'] ||
      parsed['samlp:Response']?.['saml:Assertion'];

    if (!assertion) {
      logger.warn('No Assertion element found in SAML Response');
      return res.status(400).send('Bad Request: Missing Assertion');
    }

    const attributes =
      assertion.AttributeStatement?.Attribute ||
      assertion['saml:AttributeStatement']?.['saml:Attribute'];

    if (!attributes) {
      logger.warn('No AttributeStatement found in Assertion');
      return res.status(400).send('Bad Request: Missing AttributeStatement');
    }

    /* ---------- 3️⃣  Normalise attributes ---------- */
    const attrs = {};
    const attrArray = Array.isArray(attributes) ? attributes : [attributes];

    attrArray.forEach((attr) => {
      const name = attr.Name || attr.$?.Name;
      const values = attr['AttributeValue'] || attr.$?.Value;
      const valueArray = Array.isArray(values) ? values : [values];
      attrs[name] = valueArray.map((v) => (typeof v === 'object' ? v._ : v));
    });

    // Attach to request & session
    req.saml = { attributes: attrs };
    req.session.saml = attrs;

    logger.info('SAML parsed and validated', { user: attrs['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress']?.[0] });

    next();
  } catch (err) {
    logger.error('SAML parsing error', { error: err.message });
    res.status(500).send('Internal Server Error: SAML processing failed');
  }
}

module.exports = { parseSAML };