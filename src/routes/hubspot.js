const express = require('express');
const router = express.Router();
const hubspotService = require('../services/hubspot');

// GET /api/hubspot/contacts
router.get('/contacts', async (req, res) => {
  try {
    const contacts = await hubspotService.getMarketingContacts();
    res.json(contacts);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch contacts' });
  }
});

// GET /api/hubspot/contacts/:id
router.get('/contacts/:id', async (req, res) => {
  try {
    const contact = await hubspotService.getContactById(req.params.id);
    res.json(contact);
  } catch (error) {
    res.status(404).json({ error: 'Contact not found' });
  }
});

// POST /api/hubspot/emails
router.post('/emails', async (req, res) => {
  try {
    const campaign = await hubspotService.createMarketingEmail(req.body);
    res.status(201).json(campaign);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create campaign' });
  }
});

module.exports = router;