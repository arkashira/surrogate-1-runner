import React, { useState } from 'react';

const CloudSettings = () => {
  const [provider, setProvider] = useState('aws');
  const [importStatus, setImportStatus] = useState('idle');

  const providers = [
    { value: 'aws', label: 'Amazon Web Services' },
    { value: 'gcp', label: 'Google Cloud Platform' },
    { value: 'azure', label: 'Microsoft Azure' }
  ];

  const handleProviderChange = (e) => {
    setProvider(e.target.value);
  };

  const importData = async () => {
    setImportStatus('processing');
    try {
      const response = await fetch(`/api/import?provider=${provider}`);
      if (response.ok) {
        setImportStatus('success');
      } else {
        setImportStatus('error');
      }
    } catch (err) {
      setImportStatus('error');
    }
  };

  return (
    <div className="cloud-settings">
      <h2>Cloud Provider Settings</h2>
      <div className="provider-selector">
        <label htmlFor="provider-select">Select Cloud Provider:</label>
        <select 
          id="provider-select" 
          value={provider} 
          onChange={handleProviderChange}
        >
          {providers.map(p => (
            <option key={p.value} value={p.value}>{p.label}</option>
          ))}
        </select>
      </div>
      <button onClick={importData} disabled={importStatus === 'processing'}>
        {importStatus === 'processing' ? 'Importing...' : 'Import Cost Data'}
      </button>
      {importStatus === 'success' && <p className="success">Data imported successfully</p>}
      {importStatus === 'error' && <p className="error">Failed to import data</p>}
    </div>
  );
};

export default CloudSettings;