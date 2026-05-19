const crypto = require('crypto');
const axios = require('axios');

const GITHUB_CLIENT_ID = process.env.GITHUB_CLIENT_ID;
const GITHUB_CLIENT_SECRET = process.env.GITHUB_CLIENT_SECRET;
const GITHUB_CALLBACK_URL = process.env.GITHUB_CALLBACK_URL || 'http://localhost:3000/auth/github/callback';
const STATE_SECRET = process.env.OAUTH_STATE_SECRET || 'dev-secret-change-in-production';

const stateStore = new Map();

function generateState(userId) {
  const state = crypto.randomBytes(32).toString('hex');
  const expiresAt = Date.now() + 10 * 60 * 1000;
  stateStore.set(state, { userId, expiresAt });
  return state;
}

function validateState(state) {
  const record = stateStore.get(state);
  if (!record) return null;
  if (Date.now() > record.expiresAt) {
    stateStore.delete(state);
    return null;
  }
  stateStore.delete(state);
  return record.userId;
}

function getAuthUrl(userId) {
  const state = generateState(userId);
  const params = new URLSearchParams({
    client_id: GITHUB_CLIENT_ID,
    redirect_uri: GITHUB_CALLBACK_URL,
    scope: 'repo read:user',
    state: state,
  });
  return `https://github.com/login/oauth/authorize?${params.toString()}`;
}

async function exchangeCodeForToken(code) {
  const response = await axios.post('https://github.com/login/oauth/access_token', {
    client_id: GITHUB_CLIENT_ID,
    client_secret: GITHUB_CLIENT_SECRET,
    code: code,
  }, {
    headers: {
      Accept: 'application/json',
    },
  });
  return response.data.access_token;
}

async function getUserInfo(accessToken) {
  const response = await axios.get('https://api.github.com/user', {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      Accept: 'application/json',
    },
  });
  return {
    provider: 'github',
    providerId: response.data.id.toString(),
    username: response.data.login,
    email: response.data.email,
    name: response.data.name,
    avatarUrl: response.data.avatar_url,
  };
}

async function getUserRepos(accessToken) {
  const response = await axios.get('https://api.github.com/user/repos', {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      Accept: 'application/json',
    },
    params: {
      per_page: 100,
      sort: 'updated',
    },
  });
  return response.data.map(repo => ({
    id: repo.id.toString(),
    name: repo.name,
    fullName: repo.full_name,
    private: repo.private,
    url: repo.html_url,
    defaultBranch: repo.default_branch,
    updatedAt: repo.updated_at,
  }));
}

async function getRepoDetails(accessToken, owner, repo) {
  const response = await axios.get(`https://api.github.com/repos/${owner}/${repo}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      Accept: 'application/json',
    },
  });
  return {
    id: response.data.id.toString(),
    name: response.data.name,
    fullName: response.data.full_name,
    private: response.data.private,
    url: response.data.html_url,
    defaultBranch: response.data.default_branch,
    updatedAt: response.data.updated_at,
  };
}

async function disconnectRepo(accessToken, owner, repo) {
  const response = await axios.delete(`https://api.github.com/user/repos/${owner}/${repo}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.status === 204;
}

module.exports = {
  getAuthUrl,
  exchangeCodeForToken,
  getUserInfo,
  getUserRepos,
  getRepoDetails,
  disconnectRepo,
  validateState,
};