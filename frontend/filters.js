import React, { useState } from 'react';

const Filters = () => {
  const [dateRange, setDateRange] = useState({
    startDate: new Date(),
    endDate: new Date(),
  });

  const [serviceType, setServiceType] = useState('');

  const handleDateRangeChange = (event) => {
    const { name, value } = event.target;
    setDateRange((prevDateRange) => ({ ...prevDateRange, [name]: new Date(value) }));
  };

  const handleServiceTypeChange = (event) => {
    setServiceType(event.target.value);
  };

  const applyFilters = () => {
    // Implement logic to apply filters to cost data
    console.log('Applying filters:', dateRange, serviceType);
  };

  return (
    <div>
      <label>
        Start Date:
        <input type="date" name="startDate" value={dateRange.startDate.toISOString().slice(0, 10)} onChange={handleDateRangeChange} />
      </label>
      <label>
        End Date:
        <input type="date" name="endDate" value={dateRange.endDate.toISOString().slice(0, 10)} onChange={handleDateRangeChange} />
      </label>
      <label>
        Service Type:
        <select value={serviceType} onChange={handleServiceTypeChange}>
          <option value="">All</option>
          <option value="compute">Compute</option>
          <option value="storage">Storage</option>
          <option value="networking">Networking</option>
        </select>
      </label>
      <button onClick={applyFilters}>Apply Filters</button>
    </div>
  );
};

export default Filters;