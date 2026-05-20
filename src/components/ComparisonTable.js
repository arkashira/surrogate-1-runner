import React from 'react';
import './ComparisonTable.css';

const ComparisonTable = ({ variants }) => {
  return (
    <table className="comparison-table">
      <thead>
        <tr>
          <th>Variant</th>
          <th>OpenAI Compatibility</th>
          <th>Containerization Support</th>
          <th>Integration Patterns</th>
        </tr>
      </thead>
      <tbody>
        {variants.map((variant, index) => (
          <tr key={index}>
            <td>{variant.name}</td>
            <td>{variant.openaiCompatibility ? 'Yes' : 'No'}</td>
            <td>{variant.containerizationSupport ? 'Yes' : 'No'}</td>
            <td>{variant.integrationPatterns.join(', ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ComparisonTable;