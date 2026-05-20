import React, { useState } from 'react';
import './Filter.css';

const Filter = () => {
  const [minPrice, setMinPrice] = useState(0);
  const [maxPrice, setMaxPrice] = useState(1000);
  const [keySpecs, setKeySpecs] = useState('');

  const handleMinPriceChange = (event) => {
    setMinPrice(event.target.value);
  };

  const handleMaxPriceChange = (event) => {
    setMaxPrice(event.target.value);
  };

  const handleKeySpecsChange = (event) => {
    setKeySpecs(event.target.value);
  };

  const handleFilter = () => {
    // Call API to filter components based on minPrice, maxPrice, and keySpecs
    const filteredComponents = filterComponents(minPrice, maxPrice, keySpecs);
    return filteredComponents;
  };

  return (
    <div className="filter-container">
      <label>Min Price:</label>
      <input type="number" value={minPrice} onChange={handleMinPriceChange} />
      <label>Max Price:</label>
      <input type="number" value={maxPrice} onChange={handleMaxPriceChange} />
      <label>Key Specs:</label>
      <input type="text" value={keySpecs} onChange={handleKeySpecsChange} />
      <button onClick={handleFilter}>Filter</button>
    </div>
  );
};

const filterComponents = (minPrice, maxPrice, keySpecs) => {
  // API call to filter components
  // For demonstration purposes, assume we have a list of components
  const components = [
    { name: 'Component 1', price: 100, specs: 'Spec 1' },
    { name: 'Component 2', price: 200, specs: 'Spec 2' },
    { name: 'Component 3', price: 300, specs: 'Spec 3' },
  ];

  return components.filter((component) => {
    return (
      component.price >= minPrice &&
      component.price <= maxPrice &&
      component.specs.includes(keySpecs)
    );
  });
};

export default Filter;