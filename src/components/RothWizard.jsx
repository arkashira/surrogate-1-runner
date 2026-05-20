import React, { useState } from 'react';
import { Button, Modal } from 'antd';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import { saveAs } from 'file-saver';

const RothWizard = ({ summary, calculations, irsLinks }) => {
  const [isExportModalVisible, setIsExportModalVisible] = useState(false);

  const handleExportClick = () => {
    setIsExportModalVisible(true);
  };

  const handleExportPdf = () => {
    const doc = new jsPDF();
    doc.text('Summary', 10, 10);
    doc.autoTable({ html: '#summary-table' });
    doc.text('Calculations', 10, 20);
    doc.autoTable({ html: '#calculations-table' });
    doc.text('IRS Reference Links', 10, 30);
    doc.autoTable({ html: '#irs-links-table' });
    doc.save('advisor-ready-documentation.pdf');
    setIsExportModalVisible(false);
  };

  const handleExportCsv = () => {
    const csvContent = [
      ['Summary', ...Object.values(summary)],
      ['Calculations', ...Object.values(calculations)],
      ['IRS Links', ...irsLinks],
    ];
    const blob = new Blob([csvContent.map(e => e.join(',')).join('\n')], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'advisor-ready-documentation.csv');
    setIsExportModalVisible(false);
  };

  return (
    <div>
      {/* Wizard content */}
      <Button onClick={handleExportClick} disabled={!summary || !calculations || !irsLinks}>
        Export Documentation
      </Button>
      <Modal
        title="Export Options"
        visible={isExportModalVisible}
        onCancel={() => setIsExportModalVisible(false)}
        footer={[
          <Button key="back" onClick={() => setIsExportModalVisible(false)}>
            Cancel
          </Button>,
          <Button key="submit" type="primary" onClick={handleExportPdf}>
            Export as PDF
          </Button>,
          <Button key="submit" type="primary" onClick={handleExportCsv}>
            Export as CSV
          </Button>,
        ]}
      >
        <p>Select the format you want to export:</p>
      </Modal>
    </div>
  );
};

export default RothWizard;