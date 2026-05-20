const express = require('express');
const router = express.Router();
const db = require('../db');

router.get('/brand-profiles', async (req, res) => {
  try {
    const keyword = req.query.keyword;
    const query = {
      text: `SELECT * FROM brand_profiles WHERE name ILIKE $1 OR description ILIKE $1`,
      values: [`%${keyword}%`],
    };
    const results = await db.query(query);
    res.json(results.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Error searching brand profiles' });
  }
});

module.exports = router;