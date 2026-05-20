const jwt = require('jsonwebtoken');

exports.validateToken = async (token) => {
  try {
    const decoded = jwt.verify(token, 'your_secret_key');
    // Validate decoded token here
    // ...
    return true;
  } catch (err) {
    return false;
  }
};