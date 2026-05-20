import axios from 'axios';

export const getComplianceValidationResults = async () => {
  try {
    const response = await axios.get('/api/compliance/results');
    return response.data;
  } catch (error) {
    console.error('Error fetching compliance validation results:', error);
    return [];
  }
};

export const filterAndSortResults = (results, searchText, sortField, sortOrder) => {
  let filteredResults = [...results];

  if (searchText) {
    filteredResults = filteredResults.filter((result) =>
      result.validationId.toLowerCase().includes(searchText.toLowerCase()) ||
      result.status.toLowerCase().includes(searchText.toLowerCase()) ||
      result.violations.some((violation) => violation.toLowerCase().includes(searchText.toLowerCase()))
    );
  }

  if (sortField && sortOrder) {
    filteredResults.sort((a, b) => {
      if (sortOrder === 'ascend') {
        return a[sortField] > b[sortField] ? 1 : -1;
      } else {
        return a[sortField] < b[sortField] ? 1 : -1;
      }
    });
  }

  return filteredResults;
};