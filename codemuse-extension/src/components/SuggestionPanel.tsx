import React, { useState } from 'react';
import { Editor } from 'codemirror';
import CodeInserter from '../services/CodeInserter';

interface Suggestion {
  id: string;
  preview: string;
  fullCode: string;
}

interface SuggestionPanelProps {
  suggestions: Suggestion[];
  editor: Editor;
}

const SuggestionPanel: React.FC<SuggestionPanelProps> = ({ suggestions, editor }) => {
  const [selectedSuggestionId, setSelectedSuggestionId] = useState<string | null>(null);
  const codeInserter = new CodeInserter(editor);

  const handleSuggestionClick = (suggestion: Suggestion) => {
    setSelectedSuggestionId(suggestion.id);
    codeInserter.insertCode(suggestion.fullCode);
  };

  return (
    <div style={{ height: '300px', overflowY: 'scroll' }}>
      {suggestions.map((suggestion) => (
        <div key={suggestion.id} onClick={() => handleSuggestionClick(suggestion)}>
          <pre>{suggestion.preview}</pre>
        </div>
      ))}
    </div>
  );
};

export default SuggestionPanel;