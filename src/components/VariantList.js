import React, { useState } from 'react';
import './VariantList.css';

const VariantList = ({ variants }) => {
  const [sortKey, setSortKey] = useState('');
  const [filterKey, setFilterKey] = useState('');

  const handleSortChange = (event) => {
    setSortKey(event.target.value);
  };

  const handleFilterChange = (event) => {
    setFilterKey(event.target.value);
  };

  const sortedVariants = variants.sort((a, b) => {
    if (sortKey && a[sortKey] && b[sortKey]) {
      return a[sortKey].localeCompare(b[sortKey]);
    }
    return 0;
  });

  const filteredVariants = sortedVariants.filter(variant => {
    return variant.capabilities.includes(filterKey);
  });

  return (
    <div className="variant-list">
      <div className="controls">
        <label>
          Sort By:
          <select value={sortKey} onChange={handleSortChange}>
            <option value="">None</option>
            <option value="name">Name</option>
            <option value="description">Description</option>
          </select>
        </label>
        <label>
          Filter By Capability:
          <input type="text" value={filterKey} onChange={handleFilterChange} />
        </label>
      </div>
      <ul>
        {filteredVariants.map((variant, index) => (
          <li key={index} className="variant-item">
            <h3>{variant.name}</h3>
            <p><strong>Description:</strong> {variant.description}</p>
            <p><strong>Capabilities:</strong> {variant.capabilities.join(', ')}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VariantList;