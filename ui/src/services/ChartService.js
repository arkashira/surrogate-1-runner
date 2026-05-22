import axios from 'axios';
import moment from 'moment';
import { getRevenueData, getExpenseData } from '../api/dataApi';
import { formatDateRange, isValidDateRange } from '../utils/dateUtils';

class ChartService {
  async getChartData(dateRange) {
    const formattedDateRange = formatDateRange(dateRange);
    if (!isValidDateRange(formattedDateRange.startDate, formattedDateRange.endDate)) {
      throw new Error('Invalid date range provided.');
    }

    const revenueData = await getRevenueData(formattedDateRange);
    const expenseData = await getExpenseData(formattedDateRange);

    return {
      revenue: revenueData.map((data) => ({ x: data.date, y: data.amount })),
      expense: expenseData.map((data) => ({ x: data.date, y: data.amount })),
    };
  }

  async getCustomDateRangeChartData(startDate, endDate) {
    if (!isValidDateRange(startDate, endDate)) {
      throw new Error('Invalid date range provided.');
    }

    const revenueData = await getRevenueData({ startDate, endDate });
    const expenseData = await getExpenseData({ startDate, endDate });

    return {
      revenue: revenueData.map((data) => ({ x: data.date, y: data.amount })),
      expense: expenseData.map((data) => ({ x: data.date, y: data.amount })),
    };
  }

  static async fetchChartData(startDate, endDate) {
    try {
      const response = await axios.get(`/api/financial-trends?startDate=${startDate}&endDate=${endDate}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching chart data:', error);
      throw error;
    }
  }

  static getDateRange(range) {
    if (range === '7-day') {
      return [moment().subtract(7, 'days').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')];
    } else if (range === '30-day') {
      return [moment().subtract(30, 'days').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')];
    } else {
      return range.split('-').map(date => moment(date).format('YYYY-MM-DD'));
    }
  }
}

export default ChartService;