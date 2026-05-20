const creditService = require('./creditService');

class CreditController {
  async getBalance(req, res) {
    try {
      const balances = creditService.getBalances();
      res.json({ success: true, data: balances });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'Failed to retrieve credit balances',
        details: error.message
      });
    }
  }

  async getHistory(req, res) {
    try {
      const period = parseInt(req.query.period) || 30;
      const historyData = creditService.getHistory(period);
      res.json({ success: true, data: historyData });
    } catch (error) {
      res.status(error.message.includes('Invalid') ? 400 : 500).json({
        success: false,
        error: error.message || 'Failed to retrieve usage history'
      });
    }
  }

  async getDashboard(req, res) {
    try {
      const period = parseInt(req.query.period) || 30;
      const dashboardData = creditService.getDashboardData(period);
      res.json({ success: true, data: dashboardData });
    } catch (error) {
      res.status(error.message.includes('Invalid') ? 400 : 500).json({
        success: false,
        error: error.message || 'Failed to retrieve dashboard data'
      });
    }
  }
}

module.exports = new CreditController();