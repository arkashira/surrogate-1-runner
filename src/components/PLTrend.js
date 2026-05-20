import React, { useState, useEffect } from 'react';
import PLChart from './PLChart';
import TimeRangeSelector from './TimeRangeSelector';

const PLTrend = () => {
  const [data, setData] = useState([]);
  const [timeRange, setTimeRange] = useState('3');

  useEffect(() => {
    // Fetch data based on the selected time range
    const fetchData = async () => {
      const response = await fetch(`/api/pl-data?range=${timeRange}`);
      const result = await response.json();
      setData(result);
    };

    fetchData();
  }, [timeRange]);

  return (
    <div>
      <TimeRangeSelector onRangeChange={setTimeRange} />
      <PLChart data={data} />
    </div>
  );
};

export default PLTrend;