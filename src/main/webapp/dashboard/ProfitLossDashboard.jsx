import React, { useState } from 'react';
import ProfitLossChart from './ProfitLossChart';

const ProfitLossDashboard = () => {
  const [dataSource, setDataSource] = useState('default');

  const handleDataSourceChange = (event) => {
    setDataSource(event.target.value);
  };

  return (
    <div>
      <h1>Profit & Loss Dashboard</h1>
      <select value={dataSource} onChange={handleDataSourceChange}>
        <option value="default">Default Data Source</option>
        <option value="surrogate-1">Surrogate-1 Ingest Workers</option>
      </select>
      <ProfitLossChart dataSource={dataSource} />
    </div>
  );
};

export default ProfitLossDashboard;