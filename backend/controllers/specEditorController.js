const { detectAmbiguity } = require('../services/sanity');

function processSpec(req, res) {
  const specSections = req.body.specSections; // Assuming the spec sections are sent in the request body
  
  const warnings = detectAmbiguity(specSections);

  res.json({ warnings });
}

module.exports = {
  processSpec
};