import React, { useState } from 'react';
import { ClawVariant } from '../types';

interface ComparisonTableProps {
  variants: ClawVariant[];
}

const ComparisonTable: React.FC<ComparisonTableProps> = ({ variants }) => {
  const [selectedVariants, setSelectedVariants] = useState<string[]>([]);

  const handleVariantSelection = (variantId: string) => {
    setSelectedVariants(prevSelected =>
      prevSelected.includes(variantId)
        ? prevSelected.filter(id => id !== variantId)
        : [...prevSelected, variantId]
    );
  };

  return (
    <div className="comparison-table">
      <div className="variant-selection">
        {variants.map(variant => (
          <label key={variant.id}>
            <input
              type="checkbox"
              checked={selectedVariants.includes(variant.id)}
              onChange={() => handleVariantSelection(variant.id)}
            />
            {variant.name}
          </label>
        ))}
      </div>
      <table>
        <thead>
          <tr>
            <th>Capability</th>
            {selectedVariants.map(variantId => {
              const variant = variants.find(v => v.id === variantId);
              return <th key={variantId}>{variant?.name}</th>;
            })}
          </tr>
        </thead>
        <tbody>
          {Object.keys(variants[0]?.capabilities || {}).map(capability => (
            <tr key={capability}>
              <td>{capability}</td>
              {selectedVariants.map(variantId => {
                const variant = variants.find(v => v.id === variantId);
                return (
                  <td key={`${variantId}-${capability}`}>
                    {variant?.capabilities[capability] ? '✓' : '✗'}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ComparisonTable;