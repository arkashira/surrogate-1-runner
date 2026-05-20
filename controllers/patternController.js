const Pattern = require('../models/pattern');
const k8s = require('../utils/k8s');

exports.submitPattern = async (req, res) => {
  try {
    const pattern = new Pattern(req.body);
    await pattern.save();
    res.status(201).send(pattern);
  } catch (err) {
    res.status(400).send(err);
  }
};

exports.validatePattern = async (patternId) => {
  const pattern = await Pattern.findById(patternId);
  if (!pattern) return false;

  const k8sVersion = await k8s.getVersion();
  return k8sVersion >= pattern.k8sVersion;
};