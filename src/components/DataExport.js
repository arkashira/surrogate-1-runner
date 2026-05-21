import React, { useState } from 'react';
import { encryptData, downloadFile } from './utils/dataUtils';

const DataExport = () => {
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    setExporting(true);
    try {
      // Fetch user data from local storage
      const userData = await getUserData();

      // Encrypt the user data
      const encryptedData = encryptData(userData);

      // Generate a filename for the exported data
      const filename = `userData_${new Date().toISOString()}.json`;

      // Download the encrypted data as a file
      downloadFile(encryptedData, filename);

      setExporting(false);
    } catch (error) {
      console.error('Error exporting data:', error);
      setExporting(false);
    }
  };

  return (
    <div>
      <button onClick={handleExport} disabled={exporting}>
        {exporting ? 'Exporting...' : 'Export Data'}
      </button>
    </div>
  );
};

export default DataExport;