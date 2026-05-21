import React from 'react';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import { saveAs } from 'file-saver';

const ExportToPdf = (data) => {
  const doc = new jsPDF();
  doc.autoTable({ head: [['Policy', 'Status', 'Details']], body: data });
  doc.save('compliance_report.pdf');
};

const ExportToCsv = (data) => {
  const csvContent = 'data:text/csv;charset=utf-8,' + 
    data.map(e => Object.values(e).join(',')).join('\n');
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', 'compliance_report.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link); // Clean up the dynamically created element
};

export { ExportToPdf, ExportToCsv };