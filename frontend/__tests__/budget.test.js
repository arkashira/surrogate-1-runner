/**
 * @jest-environment jsdom
 */

import { getBudget, setBudget } from '../budget.js';

describe('budget module', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('returns null when no budget set', () => {
    expect(getBudget()).toBeNull();
  });

  test('sets and retrieves budget', () => {
    setBudget(500);
    expect(getBudget()).toBe(500);
  });

  test('throws on negative budget', () => {
    expect(() => setBudget(-10)).toThrow();
  });
});