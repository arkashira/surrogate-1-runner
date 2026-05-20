import React, { useState } from 'react';
import { getVariants, getVariantColumns } from '../utils/variant_utils';

const VariantList = () => {
  const [selectedVariants, setSelectedVariants] = useState([]);
  const variants = getVariants();

  const handleSelect = (variant) => {
    setSelectedVariants(prevState => {
      if (prevState.includes(variant)) {
        return prevState.filter(v => v !== variant);
      } else {
        return [...prevState, variant];
      }
    });
  };

  return (
    <div>
      <h2>Select Variants</h2>
      <ul>
        {variants.map((variant) => (
          <li key={variant.id}>
            <button onClick={() => handleSelect(variant)}>
              {selectedVariants.includes(variant) ? 'Deselect' : 'Select'} {variant.name}
            </button>
          </li>
        ))}
      </ul>
      <ComparisonTable variants={selectedVariants} />
    </div>
  );
};

const ComparisonTable = ({ variants }) => {
  if (variants.length < 2) {
    return null;
  }

  const columns = getVariantColumns();

  return (
    <table>
      <thead>
        <tr>
          <th>Variant Name</th>
          {columns.map(column => (
            <th key={column.key}>{column.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {variants.map((variant) => (
          <tr key={variant.id}>
            <td>{variant.name}</td>
            {columns.map(column => (
              <td key={column.key}>
                {variant[column.key] === true || variant[column.key] === false ? 
                  variant[column.key] ? 'Yes' : 'No' :
                  Array.isArray(variant[column.key]) ? variant[column.key].join(', ') : variant[column.key]
                }
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default VariantList;