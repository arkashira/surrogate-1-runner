import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import ReactMarkdown from 'react-markdown';

/**
 * SourceTips component
 *
 * Displays a collapsible panel with tips for the selected source type.
 * Tips are loaded from a markdown file located at `/docs/tips/<sourceType>.md`.
 *
 * Props:
 * - sourceType (string): The currently selected source type (e.g., 'S3', 'GCS', etc.).
 * - isOpen (boolean, optional): Whether the panel should be initially open.
 * - onToggle (function, optional): Callback when the panel is toggled.
 */
const SourceTips = ({ sourceType, isOpen = false, onToggle }) => {
  const [tipsContent, setTipsContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(isOpen);

  // Fetch tips whenever sourceType changes
  useEffect(() => {
    if (!sourceType) {
      setTipsContent('');
      return;
    }

    const fetchTips = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/docs/tips/${sourceType}.md`);
        if (!response.ok) {
          throw new Error(`Failed to load tips for ${sourceType}`);
        }
        const text = await response.text();
        setTipsContent(text);
      } catch (err) {
        setError(err.message);
        setTipsContent('');
      } finally {
        setLoading(false);
      }
    };

    fetchTips();
  }, [sourceType]);

  const toggleOpen = () => {
    setOpen((prev) => !prev);
    if (onToggle) onToggle(!open);
  };

  if (!sourceType) {
    return null; // No source selected, nothing to show
  }

  return (
    <div className="source-tips">
      <button
        type="button"
        className="source-tips-toggle"
        onClick={toggleOpen}
        aria-expanded={open}
      >
        {open ? 'Hide Tips' : 'Show Tips'}
      </button>

      {open && (
        <div className="source-tips-panel">
          {loading && <p>Loading tips...</p>}
          {error && <p className="error">{error}</p>}
          {!loading && !error && (
            <ReactMarkdown>{tipsContent}</ReactMarkdown>
          )}
        </div>
      )}
    </div>
  );
};

SourceTips.propTypes = {
  sourceType: PropTypes.string.isRequired,
  isOpen: PropTypes.bool,
  onToggle: PropTypes.func,
};

export default SourceTips;