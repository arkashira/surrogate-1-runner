import React, { useState } from 'react';
import axios from 'axios';

const PolicyEditor = () => {
  const [policies, setPolicies] = useState([
    { id: 1, name: 'Data Privacy', description: 'Enforce data privacy rules.' },
    { id: 2, name: 'Model Usage', description: 'Control how models are used.' },
    { id: 3, name: 'Access Controls', description: 'Manage access permissions.' }
  ]);
  const [selectedPolicy, setSelectedPolicy] = useState(null);

  const handleApplyPolicy = async () => {
    if (!selectedPolicy) return;
    try {
      await axios.post('/api/apply-policy', { policyId: selectedPolicy.id });
      alert('Policy applied successfully.');
    } catch (error) {
      console.error('Failed to apply policy:', error);
      alert('Failed to apply policy.');
    }
  };

  return (
    <div>
      <h1>Policy Editor</h1>
      <ul>
        {policies.map(policy => (
          <li key={policy.id}>
            <label>
              <input
                type="radio"
                name="policy"
                value={policy.id}
                checked={selectedPolicy?.id === policy.id}
                onChange={() => setSelectedPolicy(policy)}
              />
              {policy.name} - {policy.description}
            </label>
          </li>
        ))}
      </ul>
      <button onClick={handleApplyPolicy}>Apply Selected Policy</button>
    </div>
  );
};

export default PolicyEditor;