const express = require('express');
const router = express.Router();
const CostinelService = require('../services/costinelService');

// Initialize service
const costinelService = new CostinelService({
  apiKey: process.env.COSTINEL_API_KEY,
  baseUrl: process.env.COSTINEL_BASE_URL,
  updateInterval: 5 * 60 * 1000,
});

// GET /api/costinel/metrics
// Fetch cost metrics for a specific service type and time range
router.get('/metrics', async (req, res) => {
  try {
    const { service_type, time_range } = req.query;
    
    if (!service_type || !time_range) {
      return res.status(400).json({
        error: 'Missing required parameters: service_type and time_range',
      });
    }

    const metrics = await costinelService.fetchCostMetrics(service_type, time_range);
    res.json({
      success: true,
      data: metrics,
      service_type,
      time_range,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

// GET /api/costinel/summary
// Get cost summary across all service types
router.get('/summary', async (req, res) => {
  try {
    const { time_range } = req.query;
    const timeRange = time_range || '24h';

    const summary = await costinelService.getCostSummary(timeRange);
    res.json({
      success: true,
      data: summary,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

// GET /api/costinel/health
// Health check endpoint
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'costinel',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
  });
});

module.exports = router;