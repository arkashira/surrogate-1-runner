import React, { useState } from 'react';
import './FilterBar.module.css';

const FilterBar = ({ categories, brands, priceRanges, specs, onFilterChange }) => {
  const [filters, setFilters] = useState({
    category: '',
    priceRange: '',
    brand: '',
    spec: ''
  });

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value
    }));
    onFilterChange({ ...filters, [name]: value });
  };

  return (
    <div className="filter-bar">
      <select name="category" value={filters.category} onChange={handleFilterChange}>
        <option value="">All Categories</option>
        {categories.map((category) => (
          <option key={category} value={category}>
            {category}
          </option>
        ))}
      </select>

      <select name="priceRange" value={filters.priceRange} onChange={handleFilterChange}>
        <option value="">All Price Ranges</option>
        {priceRanges.map((range) => (
          <option key={range} value={range}>
            {range}
          </option>
        ))}
      </select>

      <select name="brand" value={filters.brand} onChange={handleFilterChange}>
        <option value="">All Brands</option>
        {brands.map((brand) => (
          <option key={brand} value={brand}>
            {brand}
          </option>
        ))}
      </select>

      <select name="spec" value={filters.spec} onChange={handleFilterChange}>
        <option value="">All Specs</option>
        {specs.map((spec) => (
          <option key={spec} value={spec}>
            {spec}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FilterBar;