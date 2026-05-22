import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchComplianceIssues } from '../actions/complianceActions';
import { RootState } from '../reducers';

const ComplianceIssues: React.FC = () => {
  const dispatch = useDispatch();
  const complianceIssues = useSelector((state: RootState) => state.compliance.issues);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadComplianceIssues = async () => {
      await dispatch(fetchComplianceIssues());
      setLoading(false);
    };

    loadComplianceIssues();
  }, [dispatch]);

  if (loading) {
    return <div>Loading compliance issues...</div>;
  }

  return (
    <div className="compliance-issues">
      <h2>Compliance Issues</h2>
      {complianceIssues.length === 0 ? (
        <p>No compliance issues found.</p>
      ) : (
        <ul>
          {complianceIssues.map((issue) => (
            <li key={issue.id}>
              <h3>{issue.title}</h3>
              <p>{issue.description}</p>
              <p>Severity: {issue.severity}</p>
              <p>Status: {issue.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ComplianceIssues;