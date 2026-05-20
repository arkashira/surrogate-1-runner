import React, { useState, useEffect, useRef } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './Dashboard.css';

/**
 * Mock data generators – in a real implementation these would be replaced
 * with API calls fetching the founder's startup metrics and benchmark data.
 */
const generateBurnRateData = () => [
  { month: 'Jan', burn: 12000, traction: 8000 },
  { month: 'Feb', burn: 15000, traction: 11000 },
  { month: 'Mar', burn: 13000, traction: 12000 },
  { month: 'Apr', burn: 14000, traction: 13000 },
];

const generatePMFData = () => [
  { date: '2023-01-01', score: 0.2 },
  { date: '2023-02-01', score: 0.35 },
  { date: '2023-03-01', score: 0.45 },
  { date: '2023-04-01', score: 0.55 },
];

const generateBenchmarkData = () => [
  { metric: 'Burn Rate', startup: 14000, industryAvg: 13000 },
  { metric: 'Traction', startup: 13000, industryAvg: 12000 },
  { metric: 'PMF Score', startup: 0.55, industryAvg: 0.45 },
];

const Dashboard = () => {
  const [burnData, setBurnData] = useState([]);
  const [pmfData, setPmfData] = useState([]);
  const [benchmarkData, setBenchmarkData] = useState([]);
  const dashboardRef = useRef(null);

  useEffect(() => {
    // In production replace with real async fetches.
    setBurnData(generateBurnRateData());
    setPmfData(generatePMFData());
    setBenchmarkData(generateBenchmarkData());
  }, []);

  const exportPdf = async () => {
    if (!dashboardRef.current) return;
    const canvas = await html2canvas(dashboardRef.current, { scale: 2 });
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save('progress_summary.pdf');
  };

  return (
    <div className="dashboard" ref={dashboardRef}>
      <h1>Startup Validation Dashboard</h1>

      {/* Burn Rate vs Traction */}
      <section className="chart-section">
        <h2>Burn Rate vs. Traction</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={burnData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="burn" stroke="#ff7300" name="Burn Rate" />
            <Line type="monotone" dataKey="traction" stroke="#82ca9d" name="Traction" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      {/* PMF Score Progression */}
      <section className="chart-section">
        <h2>PMF Score Progression</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={pmfData}>
            <XAxis dataKey="date" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="score" stroke="#ff7300" name="PMF Score" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      {/* Benchmarking Against Similar Startups */}
      <section className="chart-section">
        <h2>Benchmarking Against Similar Startups</h2>
        <ResponsiveContainer width="100%" height={300}>
          <RadarChart data={benchmarkData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis angle={30} domain={[0, 1]} />
            <Radar
              name="Startup"
              dataKey="startup"
              stroke="#8884d8"
              fill="#8884d8"
              fillOpacity={0.6}
            />
            <Radar
              name="Industry Average"
              dataKey="industryAvg"
              stroke="#82ca9d"
              fill="#82ca9d"
              fillOpacity={0.6}
            />
            <Legend />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
      </section>

      {/* Export Button */}
      <div className="export-section">
        <button onClick={exportPdf} className="export-button">
          Export Progress Summary PDF
        </button>
      </div>
    </div>
  );
};

export default Dashboard;