# src/runner.js
const { exit } = require('process');
const { checkDependencies } = require('./dependencies');

const run = async ({ ci, ...options }) => {
  try {
    await checkDependencies(options);
  } catch (error) {
    if (ci) {
      exit(1);
    } else {
      console.error(error);
    }
  }
};

module.exports = { run };