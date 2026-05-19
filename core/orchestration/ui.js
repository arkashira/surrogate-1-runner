import React, { useState, useEffect } from 'react';
import { render } from 'react-dom';

/**
 * Simple hierarchical agent visualization.
 *
 * Expected JSON config format:
 * {
 *   "name": "root",
 *   "paused": false,
 *   "children": [
 *     { "name": "child1", "paused": true, "children": [] },
 *     { "name": "child2", "paused": false, "children": [] }
 *   ]
 * }
 *
 * The component renders a tree where each node can be paused/resumed.
 */
function AgentNode({ node, onToggle }) {
  const [expanded, setExpanded] = useState(true);

  const togglePause = () => {
    onToggle(node, !node.paused);
  };

  return (
    <div style={{ marginLeft: 20 }}>
      <div>
        <span
          style={{
            cursor: 'pointer',
            fontWeight: node.paused ? 'normal' : 'bold',
            color: node.paused ? 'gray' : 'black',
          }}
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? '▾' : '▸'} {node.name}
        </span>
        <button
          style={{ marginLeft: 8 }}
          onClick={togglePause}
        >
          {node.paused ? 'Resume' : 'Pause'}
        </button>
      </div>
      {expanded && node.children && node.children.length > 0 && (
        <div>
          {node.children.map((child, idx) => (
            <AgentNode key={idx} node={child} onToggle={onToggle} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function AgentTree({ configUrl }) {
  const [config, setConfig] = useState(null);

  useEffect(() => {
    async function fetchConfig() {
      const res = await fetch(configUrl);
      const data = await res.json();
      setConfig(data);
    }
    fetchConfig();
  }, [configUrl]);

  const handleToggle = (node, paused) => {
    node.paused = paused;
    setConfig({ ...config });
  };

  if (!config) return <div>Loading agent structure...</div>;

  return (
    <div>
      <h2>Agent Hierarchy</h2>
      <AgentNode node={config} onToggle={handleToggle} />
    </div>
  );
}

// Mount point for the UI in the orchestration page
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('agent-visualization');
  if (container) {
    render(
      <AgentTree configUrl="/static/agent-config.json" />,
      container
    );
  }
});