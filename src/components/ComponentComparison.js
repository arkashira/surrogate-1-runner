import React, { useState } from 'react';
import { filterComponents } from '../utils/filtering';

const ComponentComparison = ({ components }) => {
  const [filters, setFilters] = useState({ cpu: '', gpu: '', ram: '' });

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const filteredComponents = filterComponents(components, filters);

  return (
    <div>
      <form>
        <label>
          CPU:
          <input type="text" name="cpu" value={filters.cpu} onChange={handleFilterChange} />
        </label>
        <label>
          GPU:
          <input type="text" name="gpu" value={filters.gpu} onChange={handleFilterChange} />
        </label>
        <label>
          RAM:
          <input type="text" name="ram" value={filters.ram} onChange={handleFilterChange} />
        </label>
      </form>
      <ul>
        {filteredComponents.map((component) => (
          <li key={component.id}>
            {component.name} - CPU: {component.cpu}, GPU: {component.gpu}, RAM: {component.ram}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ComponentComparison;