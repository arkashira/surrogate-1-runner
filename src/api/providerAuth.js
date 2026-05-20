const axios = require('axios');

async function refreshToken(refreshToken) {
  // Replace with your provider’s token endpoint and credentials
  const response = await axios.post('https://api.provider.com/oauth/token', {
    grant_type: 'refresh_token',
    refresh_token: refreshToken,
    client_id: process.env.CLIENT_ID,
    client_secret: process.env.CLIENT_SECRET,
  });

  const { access_token, expires_in } = response.data;
  return { accessToken: access_token, expiresIn: expires_in };
}

module.exports = { refreshToken };