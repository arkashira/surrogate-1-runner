import React from 'react';
import { OptimizationSuggestion } from '../types';

interface Props {
  suggestions: OptimizationSuggestion[];
  onAck: (id: string) => void;
}

const OptimizationSuggestions: React.FC<Props> = ({ suggestions, onAck }) => (
  <div>
    {suggestions.map(s => (
      <div key={s.id} className="suggestion">
        <h3>{s.title}</h3>
        <p>{s.description}</p>
        <p><strong>Action:</strong> {s.action}</p>
        {s.acknowledged ? (
          <span style={{ color: 'green' }}>✅ Implemented</span>
        ) : (
          <button onClick={() => onAck(s.id)}>Mark as Implemented</button>
        )}
      </div>
    ))}
  </div>
);

export default OptimizationSuggestions;