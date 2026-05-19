const express = require('express');
const { body, query, validationResult } = require('express-validator');
const Investor = require('../models/investor');

const router = express.Router();

/**
 * GET /api/investors
 * Search, filter, and paginate investors.
 */
router.get(
  '/',
  [
    query('search').optional().isString().trim(),
    query('industry').optional().isString(),
    query('location').optional().isString(),
    query('minInvestment').optional().isFloat({ min: 0 }),
    query('maxInvestment').optional().isFloat({ min: 0 }),
    query('investmentStage').optional().isString(),
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    const {
      search,
      industry,
      location,
      minInvestment,
      maxInvestment,
      investmentStage,
      page = 1,
      limit = 20,
    } = req.query;

    const query = { isVerified: true }; // only verified investors

    /* ---------- Text search ---------- */
    if (search) {
      // Prefer $text index; fallback to regex if no index
      query.$or = [
        { $text: { $search: search, $caseSensitive: false } },
        { name: { $regex: search, $options: 'i' } },
        { company: { $regex: search, $options: 'i' } },
        { bio: { $regex: search, $options: 'i' } },
      ];
    }

    /* ---------- Industry filter ---------- */
    if (industry) {
      query.industry = { $in: industry.split(',').map(i => i.trim()) };
    }

    /* ---------- Location filter ---------- */
    if (location) {
      query.$or = [
        ...(query.$or || []),
        { location: { $regex: location, $options: 'i' } },
        { locations: { $in: [new RegExp(location, 'i')] } },
      ];
    }

    /* ---------- Investment range ---------- */
    if (minInvestment || maxInvestment) {
      query['investmentRange.min'] = {};
      if (minInvestment) query['investmentRange.min'].$gte = parseFloat(minInvestment);
      if (maxInvestment) query['investmentRange.max'] = { $lte: parseFloat(maxInvestment) };
    }

    /* ---------- Stage filter ---------- */
    if (investmentStage) {
      query.investmentStages = { $in: investmentStage.split(',').map(s => s.trim()) };
    }

    /* ---------- Pagination ---------- */
    const skip = (page - 1) * limit;

    try {
      const [investors, total] = await Promise.all([
        Investor.find(query)
          .select(
            'name company bio industry investmentRange investmentStages location locations profileImage verifiedAt'
          )
          .sort({ createdAt: -1 })
          .skip(skip)
          .limit(limit)
          .lean(),
        Investor.countDocuments(query),
      ]);

      res.json({
        success: true,
        data: investors,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit),
        },
      });
    } catch (err) {
      console.error('Investor search error:', err);
      res.status(500).json({ success: false, message: 'Server error while searching investors' });
    }
  }
);

/* ---------- Get single investor ---------- */
router.get('/:id', async (req, res) => {
  try {
    const investor = await Investor.findById(req.params.id)
      .select('-__v -createdAt -updatedAt')
      .lean();

    if (!investor) return res.status(404).json({ success: false, message: 'Investor not found' });

    res.json({ success: true, data: investor });
  } catch (err) {
    console.error('Get investor error:', err);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

/* ---------- Filter options ---------- */
router.get('/filters', async (req, res) => {
  try {
    const [industries, locations, stages] = await Promise.all([
      Investor.distinct('industry', { isVerified: true }),
      Investor.distinct('location', { isVerified: true }),
      Investor.distinct('investmentStages', { isVerified: true }),
    ]);

    res.json({
      success: true,
      data: {
        industries: industries.filter(Boolean).sort(),
        locations: locations.filter(Boolean).sort(),
        investmentStages: stages.flat().filter(Boolean).sort(),
      },
    });
  } catch (err) {
    console.error('Filter options error:', err);
    res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;