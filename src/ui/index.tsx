import React, { useEffect, useState } from 'react';
import { render } from 'react-dom';
import OptimizationSuggestions from './OptimizationSuggestions';
import { OptimizationSuggestion } from '../types';

const App: React.FC = () => {
  const [suggestions, setSuggestions] = useState<OptimizationSuggestion[]>([]);

  const load = async () => {
    const r = await fetch('/api/suggestions');
    const data = await r.json();
    setSuggestions(data.suggestions);
  };

  const ack = async (id: string) => {
    await fetch(`/api/suggestions/${id}/ack`, { method: 'POST' });
    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="app">
      <h1>Cloud Optimization Suggestions</h1>
      <OptimizationSuggestions suggestions={suggestions} onAck={ack} />
    </div>
  );
};

render(<App />, document.getElementById('app'));