const fs = require('fs');
const path = require('path');

const POLICIES_FILE_PATH = path.join(__dirname, '../config/policies.json');

function loadPolicies() {
  try {
    const data = fs.readFileSync(POLICIES_FILE_PATH, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error('Error loading policies:', err);
    return [];
  }
}

function savePolicies(policies) {
  try {
    fs.writeFileSync(POLICIES_FILE_PATH, JSON.stringify(policies, null, 2));
  } catch (err) {
    console.error('Error saving policies:', err);
  }
}

module.exports = {
  loadPolicies,
  savePolicies
};