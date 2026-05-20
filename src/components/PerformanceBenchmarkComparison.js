import React, { useState } from 'react';
import './PerformanceBenchmarkComparison.css';

const PerformanceBenchmarkComparison = ({ currentRigData, upgradeOptions }) => {
  const [selectedUpgrade, setSelectedUpgrade] = useState(null);
  const [filterCriteria, setFilterCriteria] = useState('');

  const handleUpgradeSelect = (upgrade) => {
    setSelectedUpgrade(upgrade);
  };

  const handleFilterChange = (event) => {
    setFilterCriteria(event.target.value);
  };

  const filteredData = currentRigData.filter((data) =>
    data.criteria.toLowerCase().includes(filterCriteria.toLowerCase())
  );

  return (
    <div className="performance-comparison">
      <h2>Performance Benchmark Comparison</h2>
      <input
        type="text"
        placeholder="Filter by criteria"
        value={filterCriteria}
        onChange={handleFilterChange}
      />
      <div className="current-rig">
        <h3>Current Rig</h3>
        <ul>
          {filteredData.map((data, index) => (
            <li key={index}>
              {data.criteria}: {data.performance}
            </li>
          ))}
        </ul>
      </div>
      <div className="upgrade-options">
        <h3>Upgrade Options</h3>
        <select onChange={(e) => handleUpgradeSelect(e.target.value)}>
          <option value="">Select an upgrade</option>
          {upgradeOptions.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
        {selectedUpgrade && (
          <div className="selected-upgrade">
            <h4>Selected Upgrade: {selectedUpgrade}</h4>
            <ul>
              {filteredData.map((data, index) => (
                <li key={index}>
                  {data.criteria}: {data.performance * 1.2} (Estimated)
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default PerformanceBenchmarkComparison;