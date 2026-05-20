import React, { useState, useEffect, useMemo } from 'react';
import { fetchSecurityFindings } from '../services/securityService';

interface SecurityFinding {
  accountName: string;
  region: string;
  status: string;
  findings: string[];
  recommendations: string[];
}

const SecurityDashboard: React.FC = () => {
  const [findings, setFindings] = useState<SecurityFinding[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  
  // Filter state
  const [selectedAccount, setSelectedAccount] = useState<string>('');
  const [selectedRegion, setSelectedRegion] = useState<string>('');

  // Derived options (calculated once from data)
  const accounts = useMemo(() => [...new Set(findings.map(f => f.accountName))], [findings]);
  const regions = useMemo(() => [...new Set(findings.map(f => f.region))], [findings]);

  // Derived filtered list (re-calculates when filters or data change)
  const filteredFindings = useMemo(() => {
    return findings.filter(finding => {
      const matchAccount = selectedAccount ? finding.accountName === selectedAccount : true;
      const matchRegion = selectedRegion ? finding.region === selectedRegion : true;
      return matchAccount && matchRegion;
    });
  }, [findings, selectedAccount, selectedRegion]);

  useEffect(() => {
    const getSecurityFindings = async () => {
      try {
        const data = await fetchSecurityFindings();
        setFindings(data);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    getSecurityFindings();
  }, []);

  if (loading) return <div className="p-4">Loading security posture data...</div>;

  return (
    <div className="security-dashboard">
      <h1>Security Posture Dashboard</h1>
      
      <div className="filters flex gap-4 mb-6">
        <div className="filter-group">
          <label htmlFor="account-select" className="mr-2 font-bold">Account:</label>
          <select 
            id="account-select"
            value={selectedAccount} 
            onChange={(e) => setSelectedAccount(e.target.value)}
            className="border p-1 rounded"
          >
            <option value="">All Accounts</option>
            {accounts.map(account => (
              <option key={account} value={account}>{account}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="region-select" className="mr-2 font-bold">Region:</label>
          <select 
            id="region-select"
            value={selectedRegion} 
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="border p-1 rounded"
          >
            <option value="">All Regions</option>
            {regions.map(region => (
              <option key={region} value={region}>{region}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="findings-list grid gap-4">
        {filteredFindings.length === 0 ? (
          <p>No findings match the selected filters.</p>
        ) : (
          filteredFindings.map((finding, index) => (
            <div key={`${finding.accountName}-${index}`} className="finding-card border p-4 rounded shadow">
              <h2 className="text-xl font-bold">{finding.accountName}</h2>
              <p><strong>Region:</strong> {finding.region}</p>
              <p><strong>Status:</strong> {finding.status}</p>
              
              <div className="mt-2">
                <h3 className="font-semibold">Findings:</h3>
                <ul className="list-disc pl-5">
                  {finding.findings.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="mt-2">
                <h3 className="font-semibold">Recommendations:</h3>
                <ul className="list-disc pl-5">
                  {finding.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SecurityDashboard;