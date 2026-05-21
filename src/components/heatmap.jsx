import React, { useState, useEffect } from 'react';
import './heatmap.css';

const Heatmap = () => {
  const [data, setData] = useState([]);
  const [dateRange, setDateRange] = useState([]);
  const [campaignType, setCampaignType] = useState('');

  // Fetch initial data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/marketing-data');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Failed to fetch marketing data:", error);
      }
    };
    fetchData();
  }, []);

  // Handle date range changes
  const handleDateRangeChange = (field, value) => {
    setDateRange(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Handle campaign type change
  const handleCampaignTypeChange = (e) => {
    setCampaignType(e.target.value);
  };

  // Filter data based on selected criteria
  const filteredData = data.filter(item => {
    const matchesDate = !dateRange.start || !dateRange.end || 
      (item.date >= dateRange.start && item.date <= dateRange.end);

    const matchesCampaign = !campaignType || item.campaignType === campaignType;

    return matchesDate && matchesCampaign;
  });

  return (
    <div className="heatmap-container">
      <div className="filters">
        <label htmlFor="start-date">Start Date:</label>
        <input
          id="start-date"
          type="date"
          value={dateRange.start || ''}
          onChange={(e) => handleDateRangeChange('start', e.target.value)}
        />

        <label htmlFor="end-date">End Date:</label>
        <input
          id="end-date"
          type="date"
          value={dateRange.end || ''}
          onChange={(e) => handleDateRangeChange('end', e.target.value)}
        />

        <label htmlFor="campaign-type">Campaign Type:</label>
        <select
          id="campaign-type"
          value={campaignType}
          onChange={handleCampaignTypeChange}
        >
          <option value="">All</option>
          <option value="social">Social</option>
          <option value="email">Email</option>
        </select>
      </div>

      <div className="heatmap">
        {filteredData.map((item, index) => (
          <div
            key={index}
            className="heatmap-cell"
            style={{
              backgroundColor: `rgba(255, 0, 0, ${Math.min(1, item.salesVolume / 100)})`,
            }}
          >
            <span>${item.marketingSpend}</span>
            <span>{item.salesVolume}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Heatmap;