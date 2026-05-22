/**
 * filter.js
 *
 * Provides filtering and sorting utilities for the cost insights dashboard.
 * The module exports two main functions:
 *  - filterData(data, criteria): returns a subset of data matching the criteria.
 *  - sortData(data, sortKey, ascending = true): returns data sorted by the given key.
 *
 * The data is expected to be an array of objects where each object represents
 * a cost insight or recommendation with keys such as `service`, `region`,
 * `cost`, `recommendation`, `date`, etc.
 *
 * Example usage:
 *   const filtered = filterData(insights, { service: 'EC2', region: 'us-east-1' });
 *   const sorted = sortData(filtered, 'cost', false);
 */

const DEFAULT_FILTER_CRITERIA = {
  service: null,
  region: null,
  minCost: null,
  maxCost: null,
  dateFrom: null,
  dateTo: null,
};

const DEFAULT_SORT_KEY = 'cost';

/**
 * Filters an array of data objects based on the provided criteria.
 *
 * @param {Array<Object>} data - The array of data objects to filter.
 * @param {Object} criteria - The filtering criteria.
 * @param {string|null} criteria.service - Service name to filter by.
 * @param {string|null} criteria.region - Region to filter by.
 * @param {number|null} criteria.minCost - Minimum cost threshold.
 * @param {number|null} criteria.maxCost - Maximum cost threshold.
 * @param {string|null} criteria.dateFrom - ISO date string for start of range.
 * @param {string|null} criteria.dateTo - ISO date string for end of range.
 * @returns {Array<Object>} The filtered array.
 */
export function filterData(data, criteria = {}) {
  const {
    service = DEFAULT_FILTER_CRITERIA.service,
    region = DEFAULT_FILTER_CRITERIA.region,
    minCost = DEFAULT_FILTER_CRITERIA.minCost,
    maxCost = DEFAULT_FILTER_CRITERIA.maxCost,
    dateFrom = DEFAULT_FILTER_CRITERIA.dateFrom,
    dateTo = DEFAULT_FILTER_CRITERIA.dateTo,
  } = criteria;

  return data.filter((item) => {
    if (service && item.service !== service) return false;
    if (region && item.region !== region) return false;
    if (minCost !== null && item.cost < minCost) return false;
    if (maxCost !== null && item.cost > maxCost) return false;
    if (dateFrom && new Date(item.date) < new Date(dateFrom)) return false;
    if (dateTo && new Date(item.date) > new Date(dateTo)) return false;
    return true;
  });
}

/**
 * Sorts an array of data objects by a specified key.
 *
 * @param {Array<Object>} data - The array of data objects to sort.
 * @param {string} sortKey - The key to sort by (e.g., 'cost', 'date').
 * @param {boolean} ascending - Whether to sort ascending (true) or descending (false).
 * @returns {Array<Object>} The sorted array.
 */
export function sortData(data, sortKey = DEFAULT_SORT_KEY, ascending = true) {
  const sorted = [...data].sort((a, b) => {
    const valA = a[sortKey];
    const valB = b[sortKey];

    // Handle numeric and date values
    const numA = typeof valA === 'number' ? valA : parseFloat(valA);
    const numB = typeof valB === 'number' ? valB : parseFloat(valB);

    if (!isNaN(numA) && !isNaN(numB)) {
      return ascending ? numA - numB : numB - numA;
    }

    // Fallback to string comparison
    const strA = String(valA);
    const strB = String(valB);
    if (strA < strB) return ascending ? -1 : 1;
    if (strA > strB) return ascending ? 1 : -1;
    return 0;
  });

  return sorted;
}

/**
 * Utility to toggle a filter criterion in the current criteria object.
 *
 * @param {Object} current - Current criteria object.
 * @param {string} key - Criterion key to toggle.
 * @param {any} value - New value for the criterion.
 * @returns {Object} New criteria object.
 */
export function toggleCriterion(current, key, value) {
  const newCriteria = { ...current };
  if (newCriteria[key] === value) {
    newCriteria[key] = null;
  } else {
    newCriteria[key] = value;
  }
  return newCriteria;
}