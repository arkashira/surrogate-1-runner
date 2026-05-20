import React, { useState, useEffect } from 'react';
import axios from 'axios';

function BrandSearch() {
  const [keyword, setKeyword] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get(`/api/brand-profiles?keyword=${keyword}`);
        setResults(response.data);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchResults();
  }, [keyword]);

  const handleSearch = (e) => {
    setKeyword(e.target.value);
  };

  return (
    <div>
      <input type="text" value={keyword} onChange={handleSearch} placeholder="Search brand profiles" />
      {error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <ul>
          {results.map((result) => (
            <li key={result.id}>{result.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default BrandSearch;