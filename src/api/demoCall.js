/**
 * Demo API call handler for the in-app tutorial.
 *
 * This handler serves static demo responses that are used in the
 * interactive tutorial to illustrate Surrogate-1's capabilities.
 *
 * The handler expects a query parameter `action` that selects a
 * predefined demo response. If the action is not recognized,
 * a default response is returned.
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
const { demoResponses } = require('../utils/demoResponses');

function demoCall(req, res) {
  const { action } = req.query;
  const response = demoResponses[action] || demoResponses.default;
  res.json(response);
}

module.exports = { demoCall };