const axios = require('axios');

class CostCategoryDashboard {
  constructor(apiBaseUrl, authToken) {
    this.apiBaseUrl = apiBaseUrl;
    this.authToken = authToken;
  }

  async fetchCostData() {
    try {
      const response = await axios.get(`${this.apiBaseUrl}/costs`, {
        headers: {
          'Authorization': `Bearer ${this.authToken}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching cost data:', error);
      throw error;
    }
  }

  async getMonthlyTotal() {
    const costData = await this.fetchCostData();
    return costData.total_monthly_cost || 0;
  }

  async getTopCostCategories(limit = 5) {
    const costData = await this.fetchCostData();
    const categories = costData.cost_categories || [];
    
    // Sort by cost descending and limit to top N
    return categories
      .sort((a, b) => b.cost - a.cost)
      .slice(0, limit)
      .map(category => ({
        name: category.name,
        cost: category.cost
      }));
  }

  async getCostTrend() {
    const costData = await this.fetchCostData();
    return costData.cost_trend || [];
  }

  async generateDashboardSummary() {
    try {
      const [monthlyTotal, topCategories, costTrend] = await Promise.all([
        this.getMonthlyTotal(),
        this.getTopCostCategories(),
        this.getCostTrend()
      ]);

      return {
        monthly_total: monthlyTotal,
        top_categories: topCategories,
        cost_trend: costTrend
      };
    } catch (error) {
      console.error('Error generating dashboard summary:', error);
      throw error;
    }
  }
}

module.exports = CostCategoryDashboard;