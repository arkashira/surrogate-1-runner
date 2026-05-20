/**
 * @jest-environment jsdom
 */

import { forecastCost } from '../forecast.js';

describe('forecastCost', () => {
  test('returns 0 for empty history', () => {
    expect(forecastCost([])).toBe(0);
  });

  test('calculates forecast correctly', () => {
    const history = [100, 120, 110, 130];
    // last 3 months: 120, 110, 130 -> avg = 120
    // forecast = 120 * 1.2 = 144
    expect(forecastCost(history)).toBe(144);
  });

  test('rounds to two decimals', () => {
    const history = [123.45, 67.89, 10.11];
    // avg = (123.45+67.89+10.11)/3 = 73.15
    // forecast = 73.15*1.2 = 87.78
    expect(forecastCost(history)).toBeCloseTo(87.78, 2);
  });
});