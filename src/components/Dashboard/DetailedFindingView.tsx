import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Finding } from '../../types';
import { getFindingById } from '../../services/api';

const DetailedFindingView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [finding, setFinding] = useState<Finding | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchFinding = async () => {
      try {
        const data = await getFindingById(id);
        setFinding(data);
      } catch (error) {
        console.error('Error fetching finding:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFinding();
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!finding) {
    return <div>Finding not found</div>;
  }

  return (
    <div className="detailed-finding-view">
      <h1>{finding.title}</h1>
      <p>Rule: {finding.rule}</p>
      <p>Severity: {finding.severity}</p>
      <p>Resource Type: {finding.resourceType}</p>
      <p>Date: {new Date(finding.date).toLocaleString()}</p>
      <div dangerouslySetInnerHTML={{ __html: finding.description }} />
    </div>
  );
};

export default DetailedFindingView;