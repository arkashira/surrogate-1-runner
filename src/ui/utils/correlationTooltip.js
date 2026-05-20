/**
 * Utility to generate tooltip content for revenue spikes.
 *
 * This module synthesizes the robustness of date handling with the
 * richness of business metrics display.
 *
 * Expected Input:
 *   spike: {
 *     date: string | Date,
 *     spikeValue: number,
 *     increasePct: number
 *   }
 *   correlationData: {
 *     [dateKey: string]: Array<{ variable: string, correlation: number }>
 *   }
 */

import React from 'react';

/**
 * Formats a number as a currency string.
 * (Retained from Candidate 1 for revenue context)
 * @param {number} value
 * @returns {string}
 */
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(value);
}

/**
 * Generates the tooltip content for a spike point.
 *
 * @param {Object} spike - The spike data object.
 * @param {string|Date} spike.date - The date of the spike.
 * @param {number} spike.spikeValue - The revenue value on the spike day.
 * @param {number} spike.increasePct - The day-over-day percentage increase.
 * @param {Object} correlationData - Map of date to correlation array.
 * @returns {React.ReactElement}
 */
export function renderSpikeTooltip(spike, correlationData) {
  // Robust Date Handling: Normalize date to ISO YYYY-MM-DD to ensure key lookup works
  // (Adopted from Candidate 1 to prevent timezone mismatches)
  const dateKey = new Date(spike.date).toISOString().split('T')[0];
  const correlations = correlationData[dateKey] || [];

  // Sort by absolute correlation magnitude (Consensus from both candidates)
  const topCorrelations = correlations
    .slice()
    .sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation))
    .slice(0, 3);

  return (
    <div style={{ padding: '8px', fontSize: '12px', color: '#333', backgroundColor: '#fff', border: '1px solid #e0e0e0', borderRadius: '4px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      
      {/* Header: Date and Business Metrics */}
      <div style={{ fontWeight: 'bold', marginBottom: '4px', borderBottom: '1px solid #eee', paddingBottom: '4px' }}>
        {new Date(spike.date).toLocaleDateString()}
      </div>
      
      <div style={{ marginBottom: '8px' }}>
        <span style={{ fontWeight: '500' }}>{formatCurrency(spike.spikeValue)}</span>
        <span style={{ color: '#2e7d32', marginLeft: '6px', fontWeight: 'bold' }}>
          (+{spike.increasePct.toFixed(1)}%)
        </span>
      </div>

      {/* Correlation List */}
      {topCorrelations.length > 0 ? (
        <ul style={{ margin: 0, paddingLeft: '16px', listStyle: 'disc' }}>
          {topCorrelations.map((c, idx) => (
            <li key={idx} style={{ marginBottom: '2px' }}>
              <span style={{ fontWeight: '500' }}>{c.variable}</span>
              <span style={{ color: c.correlation >= 0 ? '#1565c0' : '#c62828', marginLeft: '4px' }}>
                {c.correlation >= 0 ? '↑' : '↓'} {Math.abs(c.correlation).toFixed(2)}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <div style={{ fontStyle: 'italic', color: '#888', fontSize: '11px' }}>
          No correlation data available
        </div>
      )}
    </div>
  );
}