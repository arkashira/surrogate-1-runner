import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DateRangePicker } from 'react-dates';
import 'react-dates/initialize';
import 'react-dates/lib/css/_datepicker.css';

const CostBreakdownChart = ({ data, onFilterChange }) => {
  const [dateRange, setDateRange] = useState({ startDate: null, endDate: null });
  const [tags, setTags] = useState({});

  const filteredData = data.filter(item => {
    const dateMatch = !dateRange.startDate || !dateRange.endDate || item.date >= dateRange.startDate || item.date <= dateRange.endDate;
    const tagsMatch = Object.keys(tags).every(tag => item.tags[tag] === tags[tag]);
    return dateMatch && tagsMatch;
  });

  const handleDateChange = ({ startDate, endDate }) => {
    setDateRange({ startDate, endDate });
    onFilterChange({ startDate, endDate });
  };

  const handleTagChange = (tag, value) => {
    setTags({ ...tags, [tag]: value });
    onFilterChange({ tags: { ...tags, [tag]: value } });
  };

  return (
    <div>
      <DateRangePicker
        startDate={dateRange.startDate}
        endDate={dateRange.endDate}
        onDatesChange={handleDateChange}
      />
      <BarChart width={800} height={400} data={filteredData}>
        <Bar dataKey="AWS" fill="#8884d8" />
        <Bar dataKey="GCP" fill="#82ca9d" />
        <Bar dataKey="Azure" fill="#ffc65b" />
        <XAxis dataKey="service" />
        <YAxis />
        <Tooltip />
        <Legend />
      </BarChart>
    </div>
  );
};

export default CostBreakdownChart;