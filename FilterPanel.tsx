import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types'; // Optional if using TypeScript, but kept for compatibility

// Types for our options
interface FilterOption {
  value: string;
  label: string;
}

interface FilterPanelProps {
  industries: FilterOption[];
  stages: FilterOption[];
  locations: FilterOption[];
  onChange: (filters: { industry: string; stage: string; location: string }) => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({ 
  industries, 
  stages, 
  locations, 
  onChange 
}) => {
  const [filters, setFilters] = useState({
    industry: '',
    stage: '',
    location: ''
  });

  // Lift state up to parent whenever filters change
  useEffect(() => {
    onChange(filters);
  }, [filters, onChange]);

  const handleChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div style={styles.panel}>
      <h3 style={styles.heading}>Filter Investors</h3>
      <div style={styles.grid}>
        
        {/* Industry Select */}
        <div style={styles.group}>
          <label htmlFor="industry" style={styles.label}>Industry:</label>
          <select
            id="industry"
            value={filters.industry}
            onChange={(e) => handleChange('industry', e.target.value)}
            style={styles.select}
          >
            <option value="">All Industries</option>
            {industries.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        {/* Funding Stage Select */}
        <div style={styles.group}>
          <label htmlFor="stage" style={styles.label}>Funding Stage:</label>
          <select
            id="stage"
            value={filters.stage}
            onChange={(e) => handleChange('stage', e.target.value)}
            style={styles.select}
          >
            <option value="">All Stages</option>
            {stages.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        {/* Location Select */}
        <div style={styles.group}>
          <label htmlFor="location" style={styles.label}>Location:</label>
          <select
            id="location"
            value={filters.location}
            onChange={(e) => handleChange('location', e.target.value)}
            style={styles.select}
          >
            <option value="">All Locations</option>
            {locations.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

      </div>
    </div>
  );
};

// Basic Inline Styles for immediate actionability
const styles = {
  panel: {
    padding: '1.5rem',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
    marginBottom: '2rem',
  },
  heading: {
    marginTop: 0,
    marginBottom: '1rem',
    fontSize: '1.25rem',
    color: '#333',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1.5rem',
  },
  group: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontSize: '0.9rem',
    fontWeight: 600,
    marginBottom: '0.5rem',
    color: '#555',
  },
  select: {
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '1rem',
  }
};

export default FilterPanel;