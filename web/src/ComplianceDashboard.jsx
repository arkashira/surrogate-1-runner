import React from 'react';
import { Table, Button } from 'antd';
import { ExportToPdf, ExportToCsv } from './ExportComponents';

const ComplianceDashboard = () => {
  const [complianceData, setComplianceData] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    // Fetch compliance data from API
    fetch('/api/compliance')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setComplianceData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching compliance data:', error);
        setLoading(false); // Ensure loading state is updated on error
      });
  }, []);

  const columns = [
    {
      title: 'Policy',
      dataIndex: 'policy',
      key: 'policy',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'Details',
      dataIndex: 'details',
      key: 'details',
    },
  ];

  return (
    <div>
      <h1>Compliance Dashboard</h1>
      {loading ? (
        <p>Loading compliance data...</p>
      ) : (
        <>
          <Table dataSource={complianceData} columns={columns} />
          <div style={{ marginTop: '20px' }}>
            <Button onClick={() => ExportToPdf(complianceData)}>Export to PDF</Button>
            <Button onClick={() => ExportToCsv(complianceData)}>Export to CSV</Button>
          </div>
        </>
      )}
    </div>
  );
};

export default ComplianceDashboard;