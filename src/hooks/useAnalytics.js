// ... (existing code)

// Export functionality
const exportReport = useCallback((format = 'csv') => {
  if (!data) return null;

  // ... (existing code)

  return {
    ...(format === 'csv' ? { filename: `analytics-report.csv` } : { filename: `analytics-report.json` }),
    content,
  };
}, [data]);

return {
  // ... (existing return)
  exportReport,
};