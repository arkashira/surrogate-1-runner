const express = require('express');
const router = express.Router();
const AuditTrailGenerator = require('../logic/audit-trail-generation');

router.get('/audit-trail', (req, res) => {
  const auditTrailGenerator = new AuditTrailGenerator();
  const auditTrail = auditTrailGenerator.generateAuditTrail();
  res.json(auditTrail);
});

router.get('/audit-trail/export', (req, res) => {
  const auditTrailGenerator = new AuditTrailGenerator();
  const auditTrail = auditTrailGenerator.generateAuditTrail();
  const format = req.query.format;
  const exportedAuditTrail = auditTrailGenerator.exportAuditTrail(auditTrail, format);
  res.set("Content-Disposition", `attachment; filename="audit-trail.${format}"`);
  res.set("Content-Type", `application/${format}`);
  res.send(exportedAuditTrail);
});

router.post('/audit-trail/save', (req, res) => {
  const auditTrailGenerator = new AuditTrailGenerator();
  const auditTrail = auditTrailGenerator.generateAuditTrail();
  auditTrailGenerator.saveAuditTrail(auditTrail);
  res.json({ message: 'Audit trail saved successfully' });
});

module.exports = router;