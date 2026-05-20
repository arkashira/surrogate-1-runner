import React, { useState, useEffect } from 'react';
import * as vscode from 'vscode';

interface SettingsViewProps {
  onSave: (settings: any) => void;
}

const SettingsView: React.FC<SettingsViewProps> = ({ onSave }) => {
  const [endpointUrl, setEndpointUrl] = useState('');
  const [suggestionDepth, setSuggestionDepth] = useState('quick');

  useEffect(() => {
    // Load settings from VS Code configuration
    const config = vscode.workspace.getConfiguration('codemuse');
    setEndpointUrl(config.get('endpointUrl', ''));
    setSuggestionDepth(config.get('suggestionDepth', 'quick'));
  }, []);

  const handleSave = () => {
    // Save settings to VS Code configuration
    vscode.workspace.getConfiguration('codemuse').update('endpointUrl', endpointUrl, vscode.ConfigurationTarget.Global);
    vscode.workspace.getConfiguration('codemuse').update('suggestionDepth', suggestionDepth, vscode.ConfigurationTarget.Global);
    onSave({ endpointUrl, suggestionDepth });
  };

  return (
    <div>
      <h2>CodeMuse Settings</h2>
      <label>
        Endpoint URL:
        <input type="text" value={endpointUrl} onChange={(e) => setEndpointUrl(e.target.value)} />
      </label>
      <br />
      <label>
        Suggestion Depth:
        <select value={suggestionDepth} onChange={(e) => setSuggestionDepth(e.target.value)}>
          <option value="quick">Quick</option>
          <option value="medium">Medium</option>
          <option value="deep">Deep</option>
        </select>
      </label>
      <br />
      <button onClick={handleSave}>Save Settings</button>
    </div>
  );
};

export default SettingsView;