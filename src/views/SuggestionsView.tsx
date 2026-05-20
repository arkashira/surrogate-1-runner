
import React, { useState, useEffect } from 'react';
import { useEditor } from '@codemuse/editor';

export const SuggestionsView = () => {
  const { editorView } = useEditor();
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    // Fetch AI suggestions from server
    fetch('https://api.codemuse.ai/suggestions')
      .then((res) => res.json())
      .then((data) => setSuggestions(data));
  }, []);

  const handleSelect = (suggestion) => {
    const { start, end } = editorView.state.selection;
    const newCode = editorView.state.doc.text.slice(0, start) + suggestion + editorView.state.doc.text.slice(end);
    editorView.dispatch({ changes: { from: start, to: start + suggestion.length, insert: suggestion } });
  };

  return (
    <div>
      <h2>AI Suggestions</h2>
      <ul>
        {suggestions.map((suggestion, index) => (
          <li key={index} onClick={() => handleSelect(suggestion)}>
            {suggestion.slice(0, 3)} ...
          </li>
        ))}
      </ul>
    </div>
  );
};