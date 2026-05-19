import React, { useState, useEffect, useMemo } from 'react';
import { filterAndSort } from '../utils/filterAndSort';
import PropTypes from 'prop-types';

/**
 * InventoryTable component renders a spreadsheet-like table
 * with filtering, sorting, and real-time updates.
 *
 * Props:
 *  - data: Array of inventory record objects
 *  - columns: Array of column definitions { key, label, sortable, filterable }
 *  - pageSize: Number of rows per page (default 50)
 */
const InventoryTable = ({ data, columns, pageSize = 50 }) => {
  const [filterText, setFilterText] = useState('');
  const [sortKey, setSortKey] = useState(null);
  const [sortDir, setSortDir] = useState('asc');
  const [currentPage, setCurrentPage] = useState(1);

  // Real-time updates via polling
  useEffect(() => {
    const interval = setInterval(() => {
      // Fetch new data from an API in a real application
      // For demonstration, we trigger a re-render
      setCurrentPage((p) => p);
    }, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const filteredSortedData = useMemo(() => {
    return filterAndSort(data, filterText, sortKey, sortDir);
  }, [data, filterText, sortKey, sortDir]);

  const totalPages = Math.ceil(filteredSortedData.length / pageSize);
  const paginatedData = filteredSortedData.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  return (
    <div className="inventory-table">
      <div className="controls">
        <input
          type="text"
          placeholder="Filter..."
          value={filterText}
          onChange={(e) => {
            setFilterText(e.target.value);
            setCurrentPage(1);
          }}
        />
      </div>
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                onClick={() => col.sortable && handleSort(col.key)}
                style={{ cursor: col.sortable ? 'pointer' : 'default' }}
              >
                {col.label}
                {sortKey === col.key && (sortDir === 'asc' ? ' ▲' : ' ▼')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col.key}>{row[col.key]}</td>
              ))}
            </tr>
          ))}
          {paginatedData.length === 0 && (
            <tr>
              <td colSpan={columns.length} style={{ textAlign: 'center' }}>
                No records found
              </td>
            </tr>
          )}
        </tbody>
      </table>
      <div className="pagination">
        <button
          disabled={currentPage <= 1}
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
        >
          Prev
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          disabled={currentPage >= totalPages}
          onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
        >
          Next
        </button>
      </div>
    </div>
  );
};

InventoryTable.propTypes = {
  data: PropTypes.array.isRequired,
  columns: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      sortable: PropTypes.bool,
      filterable: PropTypes.bool,
    })
  ).isRequired,
  pageSize: PropTypes.number,
};

export default InventoryTable;