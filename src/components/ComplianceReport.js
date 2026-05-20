import React from 'react';
import axios from 'axios';

const ComplianceReport = () => {
  const [report, setReport] = React.useState(null);

  React.useEffect(() => {
    axios.get('/api/compliance-report')
      .then(response => {
        setReport(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  if (!report) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Compliance Report</h2>
      <p>Security scan results: {report.securityScanResults}</p>
      <p>Recommendations for remediation: {report.remediationRecommendations}</p>
    </div>
  );
};

export default ComplianceReport;