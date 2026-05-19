import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInvoiceSummaries } from '../actions/invoiceActions';
import { RootState } from '../store';
import { InvoiceSummary } from '../types';

const InvoiceSummaryDashboard: React.FC = () => {
  const dispatch = useDispatch();
  const invoiceSummaries = useSelector((state: RootState) => state.invoice.invoiceSummaries);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSummaries = async () => {
      await dispatch(fetchInvoiceSummaries());
      setLoading(false);
    };
    loadSummaries();
  }, [dispatch]);

  if (loading) {
    return <div>Loading invoice summaries...</div>;
  }

  return (
    <div className="invoice-summary-dashboard">
      <h1>Invoice Summaries</h1>
      <div className="summary-list">
        {invoiceSummaries.map((summary: InvoiceSummary) => (
          <div key={summary.id} className="summary-card">
            <h2>{summary.invoiceNumber}</h2>
            <p>Date: {summary.date}</p>
            <p>Amount: ${summary.amount}</p>
            <p>Status: {summary.status}</p>
            <p>Recommended Action: {summary.recommendedAction}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InvoiceSummaryDashboard;