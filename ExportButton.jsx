import React, { useState } from 'react';
import { exportAndDownload, EXPORT_FORMATS } from '../utils/exporter';

const ExportButton = ({ dashboardData, disabled = false }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [lastExport, setLastExport] = useState(null);

  const handleExport = async (format) => {
    if (!dashboardData || disabled || isExporting) return;
    setIsExporting(true);
    setShowDropdown(false);
    try {
      const filename = exportAndDownload(dashboardData, format, 'marketing-dashboard-report');
      setLastExport({ filename, format, timestamp: new Date().toISOString() });
    } catch (error) {
      console.error('Export failed:', error);
      // Display error message to user
    } finally {
      setIsExporting(false);
    }
  };

  const formatLabels = {
    [EXPORT_FORMATS.CSV]: 'CSV',
    [EXPORT_FORMATS.JSON]: 'JSON',
    [EXPORT_FORMATS.XLSX]: 'Excel (XLS)',
  };

  return (
    <div className="export-button-container" style={{ position: 'relative' }}>
      <button
        type="button"
        className="export-button"
        onClick={() => setShowDropdown(!showDropdown)}
        disabled={disabled || isExporting}
        aria-haspopup="true"
        aria-expanded={showDropdown}
      >
        {isExporting ? (
          <span className="spinner" style={{ width: '14px', height: '14px', border: '2px solid #fff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
        ) : (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
        )}
        Export Report
      </button>
      {showDropdown && (
        <div className="export-dropdown" style={{ position: 'absolute', top: '100%', right: 0, marginTop: '4px', backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '4px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', zIndex: 100, minWidth: '150px' }}>
          <ul>
            {Object.keys(formatLabels).map((format) => (
              <li key={format}>
                <button type="button" onClick={() => handleExport(format)}>
                  {formatLabels[format]}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ExportButton;