
import React from 'react';

interface SearchResultCardProps {
  title: string;
  author: string;
  tags: string[];
  snippet: string;
  matchedTerm: string;
  onClick: () => void;
}

const SearchResultCard: React.FC<SearchResultCardProps> = ({ title, author, tags, snippet, matchedTerm, onClick }) => {
  const highlightMatchedTerms = (text: string, term: string) => {
    const regex = new RegExp(`(${term})`, 'gi');
    return text.split(regex).map((part, index) => 
      regex.test(part) ? <span key={index} style={{ backgroundColor: 'yellow' }}>{part}</span> : part
    );
  };

  return (
    <div className="search-result-card" onClick={onClick}>
      <h3>{title}</h3>
      <p>Author: {author}</p>
      <p>Tags: {tags.join(', ')}</p>
      <p>Snippet: {highlightMatchedTerms(snippet, matchedTerm)}</p>
    </div>
  );
};

export default SearchResultCard;