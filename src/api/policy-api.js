const express = require('express');
const router = express.Router();
const PolicyValidation = require('../logic/policy-validation');

router.post('/policies/validate', async (req, res) => {
  try {
    const { policy } = req.body;

    if (!policy) {
      return res.status(400).json({ error: 'Policy data is required' });
    }

    const validator = new PolicyValidation(policy);
    const result = await validator.validate();

    if (result.isValid) {
      res.status(200).json({
        success: true,
        message: 'Policy is valid',
        data: result
      });
    } else {
      res.status(400).json({
        success: false,
        message: 'Policy has validation issues',
        errors: result.errors,
        warnings: result.warnings
      });
    }
  } catch (error) {
    console.error('Validation error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error during policy validation'
    });
  }
});

module.exports = router;