export const sortBuildOptions = (buildOptions, sortBy) => {
  return [...buildOptions].sort((a, b) => {
    if (sortBy === 'price') {
      return a.price - b.price;
    } else if (sortBy === 'performance') {
      return b.performance - a.performance;
    }
    // Add more sorting logic as needed
    return 0;
  });
};

export const filterBuildOptions = (sortedOptions, filters) => {
  return sortedOptions.filter((option) => {
    let isValid = true;
    Object.keys(filters).forEach((key) => {
      if (option[key] !== filters[key]) {
        isValid = false;
      }
    });
    return isValid;
  });
};