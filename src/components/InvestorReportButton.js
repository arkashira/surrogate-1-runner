import React from 'react';
import { Button } from 'react-bootstrap';
import { generateInvestorReport } from './reportApi';

const InvestorReportButton = () => {
  const tenantId = 'your-tenant-id'; // replace with actual tenant ID

  const handleGenerateReport = async () => {
    document.body.style.cursor = 'wait';
    try {
      await generateInvestorReport(tenantId);
    } finally {
      document.body.style.cursor = 'default';
    }
  };

  return (
    <Button onClick={handleGenerateReport}>
      Generate Investor Report
    </Button>
  );
};

export default InvestorReportButton;