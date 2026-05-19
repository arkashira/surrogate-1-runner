/**
 * filterAndSort
 *
 * Filters and sorts an array of objects.
 *
 * @param {Array<Object>} data - The data array
 * @param {string} filterText - Text to filter by (case-insensitive)
 * @param {string|null} sortKey - Key to sort by
 * @param {'asc'|'desc'} sortDir - Sort direction
 * @returns {Array<Object>} - Filtered and sorted array
 */
export const filterAndSort = (data, filterText, sortKey, sortDir) => {
  let result = [...data];

  // Case-insensitive filtering
  if (filterText) {
    const lower = filterText.toLowerCase();
    result = result.filter((item) =>
      Object.values(item).some(
        (val) =>
          val &&
          val
            .toString()
            .toLowerCase()
            .includes(lower)
      )
    );
  }

  // Flexible sorting
  if (sortKey) {
    result.sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      if (aVal === bVal) return 0;
      if (aVal === undefined || aVal === null) return 1;
      if (bVal === undefined || bVal === null) return -1;
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortDir === 'asc' ? aVal - bVal : bVal - aVal;
      }
      const aStr = aVal.toString();
      const bStr = bVal.toString();
      return sortDir === 'asc'
        ? aStr.localeCompare(bStr)
        : bStr.localeCompare(aStr);
    });
  }

  return result;
};