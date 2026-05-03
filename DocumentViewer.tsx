// Example usage in a parent component
import React from 'react';
import SearchResultCard from './SearchResultCard';
import DocumentViewer from './DocumentViewer';

const SearchResults = ({ results }) => {
  const [selectedDocument, setSelectedDocument] = React.useState(null);

  const handleCardClick = (url) => {
    setSelectedDocument(url);
  };

  return (
    <div>
      {results.map(result => (
        <SearchResultCard
          key={result.id}
          title={result.title}
          author={result.author}
          tags={result.tags}
          snippet={result.snippet}
          matchedTerm={result.matchedTerm}
          onClick={() => handleCardClick(result.documentUrl)}
        />
      ))}
      {selectedDocument && <DocumentViewer documentUrl={selectedDocument} />}
    </div>
  );
};

export default SearchResults;