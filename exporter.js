import { saveAs } from 'file-saver';

const EXPORT_FORMATS = {
  CSV: 'csv',
  JSON: 'json',
  XLSX: 'xlsx',
};

const convertToCSV = (data) => {
  // ...
};

const formatKPIData = (dashboardData) => {
  // ...
};

const exportReport = (dashboardData, format, filename) => {
  const data = formatKPIData(dashboardData);
  const blob = new Blob([data], { type: `application/${format}` });
  return { blob, filename, format };
};

const downloadFile = (blob, filename) => {
  saveAs(blob, filename);
};

const exportAndDownload = (dashboardData, format, filename) => {
  const { blob, filename: finalFilename } = exportReport(dashboardData, format, filename);
  downloadFile(blob, finalFilename);
  return finalFilename;
};

export { EXPORT_FORMATS, exportReport, exportAndDownload, convertToCSV, formatKPIData, downloadFile };