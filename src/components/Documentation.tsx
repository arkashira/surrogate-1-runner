import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';
import documents from '../data/documents.json'; // adjust if you fetch from an API
import './Documentation.css';

interface Doc {
  id: number | string;
  title: string;
  content: string;
  workflowName?: string;
  workflowLink?: string;
}

const Documentation: React.FC = () => {
  const [query, setQuery] = useState('');
  const [filtered, setFiltered] = useState<Doc[]>(documents);

  useEffect(() => {
    if (!query.trim()) {
      setFiltered(documents);
      return;
    }

    const lc = query.toLowerCase();
    const results = documents.filter(
      (doc) =>
        doc.title.toLowerCase().includes(lc) ||
        doc.content.toLowerCase().includes(lc)
    );
    setFiltered(results);
  }, [query]);

  return (
    <section className="documentation">
      <SearchBar onSearch={setQuery} />
      <div className="doc-list">
        {filtered.length ? (
          filtered.map((doc) => (
            <article key={doc.id} className="doc-item">
              <h3>{doc.title}</h3>
              <p>{doc.content}</p>
              {doc.workflowLink && (
                <a href={doc.workflowLink} className="workflow-link">
                  Workflow: {doc.workflowName}
                </a>
              )}
            </article>
          ))
        ) : (
          <p>No results found for “{query}”.</p>
        )}
      </div>
    </section>
  );
};

export default Documentation;