import React from 'react';

const ParserConfig = ({ parser }) => {
  return (
    <div>
      <h2>{parser.name} Configuration</h2>
      <p>Health: {parser.health}</p>
      {/* Add configuration form here */}
    </div>
  );
};

export default ParserConfig;