const express = require('express');
const router = express.Router();
const dataFetcher = require('../services/dataFetcher');

/**
 * GET /api/analytics/dashboard
 * Returns dashboard KPIs including conversion rate, traffic sources, and churn trends
 */
router.get('/dashboard', async (req, res) => {
  try {
    const data = await dataFetcher.getDashboardData();
    res.json({
      success: true,
      data: data,
      lastUpdated: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/analytics/kpis
 * Returns specific KPI metrics
 */
router.get('/kpis', async (req, res) => {
  try {
    const { type } = req.query;
    const kpis = await dataFetcher.getKPIs(type);
    res.json({
      success: true,
      data: kpis
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/analytics/traffic-sources
 * Returns traffic source breakdown
 */
router.get('/traffic-sources', async (req, res) => {
  try {
    const sources = await dataFetcher.getTrafficSources();
    res.json({
      success: true,
      data: sources
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/analytics/churn-trends
 * Returns churn trend data over time
 */
router.get('/churn-trends', async (req, res) => {
  try {
    const { period = '30d' } = req.query;
    const trends = await dataFetcher.getChurnTrends(period);
    res.json({
      success: true,
      data: trends
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/analytics/export
 * Export report in specified format (csv or json)
 */
router.get('/export', async (req, res) => {
  try {
    const { format = 'json', type = 'full' } = req.query;
    const reportData = await dataFetcher.getReportData(type);
    
    if (format === 'csv') {
      const csv = dataFetcher.convertToCSV(reportData);
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', 'attachment; filename=analytics-report.csv');
      return res.send(csv);
    }
    
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', 'attachment; filename=analytics-report.json');
    res.json(reportData);
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/analytics/refresh
 * Manually trigger a data refresh
 */
router.post('/refresh', async (req, res) => {
  try {
    await dataFetcher.refreshAllData();
    res.json({
      success: true,
      message: 'Data refresh completed',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;