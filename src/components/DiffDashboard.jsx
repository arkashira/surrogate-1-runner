import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CSVLink } from 'react-csv';

const DiffDashboard = () => {
  const [differences, setDifferences] = useState([]);
  const [filter, setFilter] = useState({ severity: '', database: '', script: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDifferences = async () => {
      try {
        const response = await axios.get('/api/differences');
        setDifferences(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching differences:', error);
        setLoading(false);
      }
    };

    fetchDifferences();

    const interval = setInterval(fetchDifferences, 60000); // Auto-refresh every minute

    return () => clearInterval(interval);
  }, []);

  const filteredDifferences = differences.filter(diff => {
    return (
      (filter.severity === '' || diff.severity === filter.severity) &&
      (filter.database === '' || diff.database === filter.database) &&
      (filter.script === '' || diff.scriptName === filter.script)
    );
  });

  const severityClass = (severity) => {
    switch (severity) {
      case 'Critical':
        return 'bg-red-500 text-white';
      case 'Warning':
        return 'bg-yellow-500 text-black';
      case 'Info':
        return 'bg-blue-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Difference Dashboard</h1>

      <div className="mb-4 flex space-x-4">
        <select
          value={filter.severity}
          onChange={(e) => setFilter({ ...filter, severity: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="">All Severities</option>
          <option value="Critical">Critical</option>
          <option value="Warning">Warning</option>
          <option value="Info">Info</option>
        </select>

        <select
          value={filter.database}
          onChange={(e) => setFilter({ ...filter, database: e.target.value })}
          className="p-2 border rounded"
        >
          <option value="">All Databases</option>
          <option value="Database1">Database1</option>
          <option value="Database2">Database2</option>
        </select>

        <input
          type="text"
          placeholder="Filter by script name"
          value={filter.script}
          onChange={(e) => setFilter({ ...filter, script: e.target.value })}
          className="p-2 border rounded"
        />
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="py-2 px-4 border">Severity</th>
                  <th className="py-2 px-4 border">Database</th>
                  <th className="py-2 px-4 border">Script Name</th>
                  <th className="py-2 px-4 border">Details</th>
                  <th className="py-2 px-4 border">Logs</th>
                </tr>
              </thead>
              <tbody>
                {filteredDifferences.map((diff, index) => (
                  <tr key={index}>
                    <td className={`py-2 px-4 border ${severityClass(diff.severity)}`}>
                      {diff.severity}
                    </td>
                    <td className="py-2 px-4 border">{diff.database}</td>
                    <td className="py-2 px-4 border">{diff.scriptName}</td>
                    <td className="py-2 px-4 border">
                      <a
                        href={`/scripts/${diff.scriptName}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        View Script
                      </a>
                    </td>
                    <td className="py-2 px-4 border">
                      <a
                        href={`/logs/${diff.database}/${diff.scriptName}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        View Logs
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-4">
            <CSVLink
              data={filteredDifferences}
              filename="differences.csv"
              className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
            >
              Export to CSV
            </CSVLink>
          </div>
        </>
      )}
    </div>
  );
};

export default DiffDashboard;