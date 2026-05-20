import React, { useState, useEffect, ChangeEvent } from 'react';
import debounce from 'lodash/debounce';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = 'Search documentation…',
}) => {
  const [input, setInput] = useState('');

  // Debounce the callback so we don’t flood the parent with events
  const debouncedSearch = React.useMemo(
    () => debounce(onSearch, 300),
    [onSearch]
  );

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setInput(val);
    debouncedSearch(val);
  };

  // Clean up the debounce on unmount
  useEffect(() => () => debouncedSearch.cancel(), [debouncedSearch]);

  return (
    <div className="search-bar">
      <input
        type="text"
        value={input}
        onChange={handleChange}
        placeholder={placeholder}
        aria-label="Search documentation"
      />
    </div>
  );
};

export default SearchBar;