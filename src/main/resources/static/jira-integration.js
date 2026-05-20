/**
 * Unified Jira integration utilities.
 *
 * Features
 * ────────
 * • Create a Jira issue (v3 API)
 * • Link a knowledge article (remote link)
 * • Basic Auth via env vars
 * • Early validation of configuration
 *
 * Environment variables
 * ─────────────────────
 *   JIRA_BASE_URL   – Base URL of the Jira instance (e.g. https://your-domain.atlassian.net)
 *   JIRA_USER_EMAIL – Email address of the Jira user
 *   JIRA_API_TOKEN  – API token for the user
 *
 * Example usage
 * ─────────────
 *   const { createIssue, linkArticle } = require('./jira-integration');
 *
 *   const issueKey = await createIssue({
 *     projectKey: 'PROJ',
 *     summary: 'New issue from knowledge article',
 *     description: 'Created via API',
 *     issuetype: 'Task',
 *   });
 *
 *   await linkArticle(issueKey, 'https://knowledge.example.com/article/123');
 */

const fetch = require('node-fetch');

const {
  JIRA_BASE_URL = 'https://your-domain.atlassian.net',
  JIRA_USER_EMAIL,
  JIRA_API_TOKEN,
} = process.env;

// ---------------------------------------------------------------------------
// Configuration validation
// ---------------------------------------------------------------------------

if (!JIRA_USER_EMAIL || !JIRA_API_TOKEN) {
  console.warn(
    '⚠️  Jira integration is not fully configured. Set JIRA_USER_EMAIL and JIRA_API_TOKEN to enable Jira operations.'
  );
}

// ---------------------------------------------------------------------------
// Helper: authenticated request
// ---------------------------------------------------------------------------

/**
 * Perform an authenticated request against the Jira REST API.
 *
 * @param {string} path   – API path (e.g. '/rest/api/3/issue')
 * @param {string} method – HTTP method
 * @param {Object} body   – Request body (will be JSON.stringified)
 * @returns {Promise<Object>} – Parsed JSON response
 */
async function jiraRequest(path, method = 'GET', body = null) {
  const url = `${JIRA_BASE_URL}${path}`;
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  };

  if (JIRA_USER_EMAIL && JIRA_API_TOKEN) {
    const auth = Buffer.from(`${JIRA_USER_EMAIL}:${JIRA_API_TOKEN}`).toString('base64');
    headers.Authorization = `Basic ${auth}`;
  }

  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(url, options);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Jira API error ${response.status}: ${errorText}`);
  }

  // Some endpoints return 204 No Content
  if (response.status === 204) return null;
  return response.json();
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Create a new Jira issue.
 *
 * @param {Object} params
 * @param {string} params.projectKey
 * @param {string} params.summary
 * @param {string} params.description
 * @param {string} [params.issuetype='Task']
 * @returns {Promise<string>} – The key of the created issue (e.g. PROJ-123)
 */
async function createIssue({
  projectKey,
  summary,
  description,
  issuetype = 'Task',
}) {
  if (!JIRA_BASE_URL) {
    throw new Error('Jira integration not configured.');
  }

  const payload = {
    fields: {
      project: { key: projectKey },
      summary,
      description,
      issuetype: { name: issuetype },
    },
  };

  const result = await jiraRequest('/rest/api/3/issue', 'POST', payload);
  return result.key;
}

/**
 * Link a knowledge article to an existing Jira issue.
 *
 * @param {string} issueKey   – Key of the Jira issue (e.g. PROJ-123)
 * @param {string} articleUrl – URL or key of the knowledge article
 * @returns {Promise<void>}
 */
async function linkArticle(issueKey, articleUrl) {
  if (!JIRA_BASE_URL) {
    throw new Error('Jira integration not configured.');
  }

  const payload = {
    type: { name: 'Related' },
    // The article can be any URL; Jira will store it as a remote link
    object: {
      url: articleUrl,
      title: `Knowledge Article: ${articleUrl}`,
    },
  };

  await jiraRequest(`/rest/api/3/issue/${issueKey}/remotelink`, 'POST', payload);
}

module.exports = {
  createIssue,
  linkArticle,
};