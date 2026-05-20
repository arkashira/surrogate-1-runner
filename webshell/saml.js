const passport = require('passport');
const SamlStrategy = require('passport-saml').Strategy;
const express = require('express');
const session = require('express-session');

// ------------------------------------------------------------------
// 1️⃣  Load configuration from the environment
// ------------------------------------------------------------------
const {
  SAML_ENTRY_POINT,          // IdP SSO URL
  SAML_ISSUER,               // SP entity ID
  SAML_CALLBACK_URL,         // ACS endpoint
  SAML_CERT,                 // IdP public certificate (PEM)
  SAML_PRIVATE_CERT,         // SP private key (optional)
  SAML_DECRYPTION_PVK,       // SP decryption key (optional)
  SAML_SESSION_SECRET,       // secret for express‑session
} = process.env;

// Basic validation – fail fast if something is missing
if (!SAML_ENTRY_POINT || !SAML_ISSUER || !SAML_CALLBACK_URL || !SAML_CERT) {
  throw new Error(
    'Missing required SAML configuration. Please set SAML_ENTRY_POINT, SAML_ISSUER, SAML_CALLBACK_URL, and SAML_CERT.'
  );
}

// ------------------------------------------------------------------
// 2️⃣  Configure the passport‑saml strategy
// ------------------------------------------------------------------
const samlStrategy = new SamlStrategy(
  {
    entryPoint: SAML_ENTRY_POINT,
    issuer: SAML_ISSUER,
    callbackUrl: SAML_CALLBACK_URL,
    cert: SAML_CERT,
    privateCert: SAML_PRIVATE_CERT,
    decryptionPvk: SAML_DECRYPTION_PVK,
    // Optional: forceAuthn, wantAuthnRequestsSigned, etc.
  },
  // Verify callback – receives the SAML profile and must call `done`
  (profile, done) => {
    // Map the SAML profile to a lightweight user object
    const user = {
      id: profile.nameID,
      email:
        profile.email ||
        profile['http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'] ||
        '',
      displayName: profile.displayName || profile.cn || '',
    };
    return done(null, user);
  }
);

// ------------------------------------------------------------------
// 3️⃣  Passport serialisation / deserialisation
// ------------------------------------------------------------------
passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((obj, done) => done(null, obj));

// ------------------------------------------------------------------
// 4️⃣  Express app that owns the session & passport middleware
// ------------------------------------------------------------------
const app = express();
app.use(
  session({
    secret: SAML_SESSION_SECRET || 'change-me-in-production',
    resave: false,
    saveUninitialized: false,
  })
);
app.use(passport.initialize());
app.use(passport.session());

// ------------------------------------------------------------------
// 5️⃣  Helper functions that the router will call
// ------------------------------------------------------------------
/**
 * Redirect the user to the IdP for authentication.
 */
function redirectToLogin(req, res) {
  passport.authenticate('saml', { failureRedirect: '/saml/login/failure' })(req, res);
}

/**
 * Process the SAML assertion (ACS) – this is called by the router.
 * It returns a promise that resolves to the user object or rejects on error.
 */
function processAssertion(req) {
  return new Promise((resolve, reject) => {
    passport.authenticate('saml', (err, user, info) => {
      if (err) {
        return reject(err);
      }
      if (!user) {
        return reject(new Error('SAML assertion did not contain a user'));
      }
      return resolve(user);
    })(req, req.res);
  });
}

module.exports = {
  redirectToLogin,
  processAssertion,
  passport, // expose for potential future use
  app,      // expose the configured express app (optional)
};