import React, { useState, useEffect } from 'react';
import { generateReport } from '../utils/reporting';
import { saveAs } from 'file-saver';
import { scheduleReport, loadScheduleQueue } from '../utils/scheduler';

export default function ReportGenerator({ inventoryData }) {
  const [format, setFormat] = useState('csv');
  const [includeHeaders, setIncludeHeaders] = useState(true);
  const [scheduleTime, setScheduleTime] = useState(''); // HH:MM 24‑h

  // Load any persisted schedule queue on mount
  useEffect(() => {
    loadScheduleQueue();
  }, []);

  const handleGenerate = async () => {
    const payload = await generateReport(inventoryData, { format, includeHeaders });

    const mime = format === 'csv' ? 'text/csv' : 'application/pdf';
    const blob = new Blob([payload], { type: mime });
    saveAs(blob, `inventory_report.${format}`);
  };

  const handleSchedule = () => {
    if (!scheduleTime) {
      alert('Please pick a time to schedule the report.');
      return;
    }
    // Persist the job – in a real app this would push to a server or cron job
    scheduleReport({ format, includeHeaders, scheduleTime, data: inventoryData });
    alert(`Report scheduled for ${scheduleTime}.`);
  };

  return (
    <div className="report-generator">
      <h2>Inventory Report Generator</h2>

      <label>
        Format:
        <select value={format} onChange={e => setFormat(e.target.value)}>
          <option value="csv">CSV</option>
          <option value="pdf">PDF</option>
        </select>
      </label>

      <label>
        <input
          type="checkbox"
          checked={includeHeaders}
          onChange={e => setIncludeHeaders(e.target.checked)}
        />
        Include Headers
      </label>

      <label>
        Schedule (HH:MM 24h):
        <input
          type="time"
          value={scheduleTime}
          onChange={e => setScheduleTime(e.target.value)}
        />
      </label>

      <div className="buttons">
        <button onClick={handleGenerate}>Generate Report</button>
        <button onClick={handleSchedule}>Schedule Report</button>
      </div>
    </div>
  );
}