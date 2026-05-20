const express = require('express');
const router = express.Router();

router.post('/:serviceName', async (req, res) => {
  const serviceName = req.params.serviceName;

  try {
    // Simulate service update process
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulate delay

    // Return success response
    res.status(200).json({ message: `${serviceName} updated successfully` });
  } catch (error) {
    console.error('Error updating service:', error);
    res.status(500).json({ message: 'Error updating service' });
  }
});

module.exports = router;