/**
 * Pricing Analysis Module
 * Identifies market trends and competitor pricing strategies
 * 
 * Acceptance Criteria:
 * - Analysis performed on at least 3 product categories
 * - Analysis performed on at least 5 competitors
 * - Analysis updated weekly
 * 
 * Expected data format:
 * [
 *   {
 *     category: 'Electronics',
 *     competitor: 'CompetitorA',
 *     price: 199.99,
 *     date: '2024-04-01T00:00:00Z'
 *   },
 *   ...
 * ]
 */

const fs = require('fs');
const path = require('path');

// Configuration - easily adjustable constants
const CONFIG = {
  MIN_CATEGORIES: 3,
  MIN_COMPETITORS: 5,
  UPDATE_INTERVAL_DAYS: 7,
  DATA_DIR: path.join(__dirname, '../../data/pricing'),
  OUTPUT_DIR: path.join(__dirname, '../../output/analysis'),
  TREND_THRESHOLD_PERCENT: 1  // 1% change triggers trend
};

// Predefined product categories
const PRODUCT_CATEGORIES = [
  'Electronics',
  'Apparel',
  'Home',
  'Sports',
  'Toys'
];

/**
 * Group data by category and competitor.
 * @param {Array} data
 * @returns {Object} nested map: category -> competitor -> array of records
 */
function groupByCategoryAndCompetitor(data) {
  const map = {};
  data.forEach((record) => {
    const { category, competitor } = record;
    if (!map[category]) {
      map[category] = {};
    }
    if (!map[category][competitor]) {
      map[category][competitor] = [];
    }
    map[category][competitor].push(record);
  });
  return map;
}

/**
 * Calculate average price for an array of records.
 * @param {Array} records
 * @returns {number}
 */
function averagePrice(records) {
  if (!records.length) return 0;
  const sum = records.reduce((acc, r) => acc + r.price, 0);
  return sum / records.length;
}

/**
 * Determine trend between two price points.
 * @param {number} oldPrice
 * @param {number} newPrice
 * @returns {string} 'increase' | 'decrease' | 'stable'
 */
function determineTrend(oldPrice, newPrice) {
  if (oldPrice === 0) return 'stable';
  const diff = newPrice - oldPrice;
  const pct = (diff / oldPrice) * 100;
  if (pct > CONFIG.TREND_THRESHOLD_PERCENT) return 'increase';
  if (pct < -CONFIG.TREND_THRESHOLD_PERCENT) return 'decrease';
  return 'stable';
}

/**
 * Validate input data meets minimum requirements.
 * @param {Array} data
 * @throws {Error} If validation fails
 */
function validateData(data) {
  if (!Array.isArray(data)) {
    throw new TypeError('Data must be an array');
  }

  const categories = new Set(data.map((d) => d.category));
  if (categories.size < CONFIG.MIN_CATEGORIES) {
    throw new Error(`At least ${CONFIG.MIN_CATEGORIES} categories required`);
  }

  const competitors = new Set(data.map((d) => d.competitor));
  if (competitors.size < CONFIG.MIN_COMPETITORS) {
    throw new Error(`At least ${CONFIG.MIN_COMPETITORS} competitors required`);
  }
}

/**
 * Analyze pricing trends.
 * @param {Array} data - Array of pricing records
 * @returns {Object} Analysis results
 * 
 * Result structure:
 * {
 *   categories: {
 *     [category]: {
 *       competitors: {
 *         [competitor]: {
 *           averagePrice: number,
 *           trend: 'increase' | 'decrease' | 'stable'
 *         }
 *       }
 *     }
 *   }
 * }
 */
function analyzeTrends(data) {
  // Validate input
  validateData(data);

  const grouped = groupByCategoryAndCompetitor(data);
  const result = { categories: {} };

  Object.entries(grouped).forEach(([category, compMap]) => {
    result.categories[category] = { competitors: {} };
    
    Object.entries(compMap).forEach(([competitor, records]) => {
      // Sort by date ascending
      const sorted = records
        .map((r) => ({ ...r, date: new Date(r.date) }))
        .sort((a, b) => a.date - b.date);

      // Compute overall average price
      const avg = averagePrice(sorted);

      // Determine trend: compare last week vs previous week
      const weeks = {};
      sorted.forEach((r) => {
        const week = Math.floor(r.date.getTime() / (7 * 24 * 60 * 60 * 1000));
        if (!weeks[week]) weeks[week] = [];
        weeks[week].push(r);
      });
      
      const weekKeys = Object.keys(weeks).sort((a, b) => a - b);
      let trend = 'stable';
      
      if (weekKeys.length >= 2) {
        const prevWeekAvg = averagePrice(weeks[weekKeys[weekKeys.length - 2]]);
        const lastWeekAvg = averagePrice(weeks[weekKeys[weekKeys.length - 1]]);
        trend = determineTrend(prevWeekAvg, lastWeekAvg);
      }

      result.categories[category].competitors[competitor] = {
        averagePrice: parseFloat(avg.toFixed(2)),
        trend
      };
    });
  });

  return result;
}

/**
 * Save analysis results to output directory.
 * @param {Object} results - Analysis results
 * @param {string} filename - Output filename
 */
function saveResults(results, filename = 'trends.json') {
  if (!fs.existsSync(CONFIG.OUTPUT_DIR)) {
    fs.mkdirSync(CONFIG.OUTPUT_DIR, { recursive: true });
  }
  const filepath = path.join(CONFIG.OUTPUT_DIR, filename);
  fs.writeFileSync(filepath, JSON.stringify(results, null, 2));
  return filepath;
}

module.exports = {
  analyzeTrends,
  saveResults,
  CONFIG,
  PRODUCT_CATEGORIES
};