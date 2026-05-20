import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * DownloadButton component renders a button that, when clicked,
 * initiates a download of the signed compliance PDF.
 *
 * Props:
 * - docId (string): Identifier of the document to download.
 * - buttonText (string, optional): Text to display on the button.
 * - disabled (bool, optional): Whether the button is disabled.
 * - onError (function, optional): Callback for error handling.
 *
 * The component handles fetch errors and displays a simple
 * alert to the user. In a real application, you might replace
 * alerts with a toast notification system.
 */
const DownloadButton = ({ docId, buttonText = "Download PDF", disabled = false, onError }) => {
  const [loading, setLoading] = useState(false);

  const handleDownload = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/download/${encodeURIComponent(docId)}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/pdf',
        },
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Document not found');
        }
        throw new Error(`Server returned ${response.status}`);
      }

      // Check content type to ensure it's actually a PDF
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/pdf')) {
        throw new Error('Invalid response: not a PDF file');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${docId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      const errorMessage = err.message || 'Failed to download the PDF. Please try again.';
      alert(errorMessage);
      if (onError) {
        onError(err);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleDownload}
      disabled={disabled || loading}
      className="download-button"
      aria-label={loading ? 'Downloading PDF' : `Download ${buttonText}`}
    >
      {loading ? 'Downloading...' : buttonText}
    </button>
  );
};

DownloadButton.propTypes = {
  docId: PropTypes.string.isRequired,
  buttonText: PropTypes.string,
  disabled: PropTypes.bool,
  onError: PropTypes.func,
};

export default DownloadButton;