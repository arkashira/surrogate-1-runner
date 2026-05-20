import React from 'react';

const TimeRangeSelector = ({ onRangeChange }) => {
  const handleChange = (event) => {
    onRangeChange(event.target.value);
  };

  return (
    <div>
      <label htmlFor="time-range">Select Time Range: </label>
      <select id="time-range" onChange={handleChange}>
        <option value="1">1 Week</option>
        <option value="2">2 Weeks</option>
        <option value="1">1 Month</option>
        <option value="3">3 Months</option>
        <option value="6">6 Months</option>
        <option value="12">12 Months</option>
      </select>
    </div>
  );
};

export default TimeRangeSelector;