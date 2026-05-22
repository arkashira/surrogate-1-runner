import React, { useState } from 'react';

const Search = ({ onSearch }) => {
  const [value, setValue] = useState('');

  const handleChange = (event) => {
    setValue(event.target.value);
    onSearch(event.target.value);
  };

  return (
    <div className="search">
      <input
        type="text"
        placeholder="Search the guide..."
        value={value}
        onChange={handleChange}
      />
    </div>
  );
};

export default Search;