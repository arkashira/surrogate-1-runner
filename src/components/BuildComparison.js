import React, { useState } from 'react';
import { sortBuildOptions, filterBuildOptions } from '../utils/sorting';

const BuildComparison = ({ buildOptions }) => {
  const [selectedSort, setSelectedSort] = useState('price');
  const [filters, setFilters] = useState({});

  const handleSortChange = (event) => {
    setSelectedSort(event.target.value);
  };

  const handleFilterChange = (event) => {
    setFilters({ ...filters, [event.target.name]: event.target.value });
  };

  const sortedOptions = sortBuildOptions(buildOptions, selectedSort);
  const filteredOptions = filterBuildOptions(sortedOptions, filters);

  return (
    <div>
      <h1>Build Comparison</h1>
      <select value={selectedSort} onChange={handleSortChange}>
        <option value="price">Price</option>
        <option value="performance">Performance</option>
        {/* Add more sorting options as needed */}
      </select>

      <div>
        {/* Render filter options based on available attributes */}
        <input type="text" name="filter1" onChange={handleFilterChange} placeholder="Filter by attribute 1" />
        {/* Add more filter inputs as needed */}
      </div>

      <ul>
        {filteredOptions.map((option, index) => (
          <li key={index}>
            <h2>{option.name}</h2>
            <p>Price: ${option.price}</p>
            <p>Performance: {option.performance}</p>
            {/* Display other relevant details */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BuildComparison;