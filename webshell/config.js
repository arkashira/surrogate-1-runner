module.exports = {
  /** Groups that are allowed to use the web‑shell */
  allowedGroups: ['devops', 'admin'],

  /** Path to the IdP X.509 certificate (PEM) used for signature validation */
  idpCertPath: require('path').resolve(__dirname, 'saml-idp-cert.pem'),

  /** Express session secret – change this in production! */
  sessionSecret: 'CHANGE_ME_TO_A_RANDOM_STRING',
};