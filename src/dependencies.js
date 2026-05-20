# src/dependencies.js
const { check } = require('semver');

const checkDependencies = async ({ dependencies }) => {
  for (const [name, version] of Object.entries(dependencies)) {
    try {
      await check(name, version);
    } catch (error) {
      throw new Error(`Missing dependency: ${name}`);
    }
  }
};

module.exports = { checkDependencies };