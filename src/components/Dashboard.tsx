import React, { useEffect, useState } from 'react';
import { fetchCostData } from '../services/costService';
import CostChart from './CostChart';
import DateRangePicker from './DateRangePicker';
import ServiceFilter from './ServiceFilter';

const Dashboard: React.FC = () => {
  const [costData, setCostData] = useState<any[]>([]);
  const [dateRange, setDateRange] = useState<[Date, Date]>([new Date(), new Date()]);
  const [serviceType, setServiceType] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchCostData(dateRange, serviceType);
      setCostData(data);
    };

    fetchData();
    const interval = setInterval(fetchData, 300000); // 5 minutes

    return () => clearInterval(interval);
  }, [dateRange, serviceType]);

  return (
    <div className="dashboard">
      <h1>Real-time Cost Data</h1>
      <DateRangePicker onChange={setDateRange} />
      <ServiceFilter onChange={setServiceType} />
      <CostChart data={costData} />
    </div>
  );
};

export default Dashboard;