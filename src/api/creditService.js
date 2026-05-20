class CreditService {
  constructor() {
    this.creditStore = {
      balances: {
        bulk: 15000,
        monthly: 5000
      },
      usageHistory: this.generateMockHistory()
    };
  }

  generateMockHistory() {
    const history = [];
    const now = new Date();

    for (let i = 364; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);

      history.push({
        date: date.toISOString().split('T')[0],
        bulkUsed: Math.floor(Math.random() * 200) + 50,
        monthlyUsed: Math.floor(Math.random() * 100) + 20,
        bulkRemaining: Math.floor(Math.random() * 500) + 14000,
        monthlyRemaining: Math.floor(Math.random() * 200) + 4500
      });
    }

    return history;
  }

  getBalances() {
    return {
      bulk: {
        current: this.creditStore.balances.bulk,
        label: 'Bulk Credits',
        type: 'bulk'
      },
      monthly: {
        current: this.creditStore.balances.monthly,
        label: 'Monthly Credits',
        type: 'monthly'
      },
      lastUpdated: new Date().toISOString()
    };
  }

  getHistory(period = 30) {
    const validPeriods = [30, 90, 365];
    if (!validPeriods.includes(period)) {
      throw new Error('Invalid period. Supported values: 30, 90, 365');
    }

    const history = this.creditStore.usageHistory.slice(-period);
    return {
      period,
      history,
      aggregates: this.calculateAggregates(history)
    };
  }

  calculateAggregates(history) {
    const totalBulkUsed = history.reduce((sum, day) => sum + day.bulkUsed, 0);
    const totalMonthlyUsed = history.reduce((sum, day) => sum + day.monthlyUsed, 0);

    return {
      totalBulkUsed,
      totalMonthlyUsed,
      avgDailyBulk: Math.round(totalBulkUsed / history.length),
      avgDailyMonthly: Math.round(totalMonthlyUsed / history.length),
      trend: totalBulkUsed > totalMonthlyUsed ? 'bulk_heavier' : 'monthly_heavier'
    };
  }

  getDashboardData(period = 30) {
    return {
      balances: this.getBalances(),
      ...this.getHistory(period),
      generatedAt: new Date().toISOString()
    };
  }
}

module.exports = new CreditService();