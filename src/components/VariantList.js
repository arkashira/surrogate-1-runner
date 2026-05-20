import React, { useState } from 'react';
import './VariantList.css';

const VariantList = ({ variants }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');

  const filteredVariants = variants.filter(variant =>
    variant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    variant.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedVariants = filteredVariants.sort((a, b) => {
    if (sortBy === 'name') {
      return a.name.localeCompare(b.name);
    } else if (sortBy === 'description') {
      return a.description.localeCompare(b.description);
    }
    return 0;
  });

  return (
    <div className="variant-list">
      <input
        type="text"
        placeholder="Search by name or description..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="name">Sort by Name</option>
        <option value="description">Sort by Description</option>
      </select>
      <ul>
        {sortedVariants.map((variant, index) => (
          <li key={index}>
            <strong>{variant.name}</strong>: {variant.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VariantList;