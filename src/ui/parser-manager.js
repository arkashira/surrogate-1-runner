import React, { useState, useEffect } from 'react';
import ParserConfig from './parser-config';

const ParserManager = () => {
  const [parsers, setParsers] = useState([]);

  useEffect(() => {
    // Fetch parsers from API
    fetch('/api/parsers')
      .then(response => response.json())
      .then(data => setParsers(data));
  }, []);

  const handleAddParser = (parser) => {
    setParsers([...parsers, parser]);
  };

  return (
    <div>
      <h1>Parser Manager</h1>
      <ul>
        {parsers.map(parser => (
          <li key={parser.id}>
            {parser.name} - Health: {parser.health}
            <ParserConfig parser={parser} />
          </li>
        ))}
      </ul>
      <button onClick={() => handleAddParser({ id: Date.now(), name: 'New Parser', health: 'Unknown' })}>
        Add Parser
      </button>
    </div>
  );
};

export default ParserManager;