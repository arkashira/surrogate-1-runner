import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

/**
 * Pure deterministic estimator.
 *
 * @param {Array<{value:number|string, multiplier?:number|string}>} items
 * @returns {{ total:number, breakdown:{ Fixed:number, Variable:number, Buffer:number } }}
 *
 * Logic (demo‑style, easy to replace with a real service):
 *   • 60 % of the raw sum → Fixed
 *   • 30 % of the remainder → Variable
 *   • Whatever is left      → Buffer
 */
export function calculateEstimate(items) {
  if (!Array.isArray(items) || items.length === 0) {
    return { total: 0, breakdown: { Fixed: 0, Variable: 0, Buffer: 0 } };
  }

  const rawSum = items.reduce((acc, it) => {
    const v = Number(it.value) || 0;
    const m = Number(it.multiplier) || 1;
    return acc + v * m;
  }, 0);

  const fixed = Math.min(0.6 * rawSum, rawSum);
  const variable = Math.min(0.3 * (rawSum - fixed), rawSum - fixed);
  const buffer = Math.max(rawSum - fixed - variable, 0);

  return {
    total: fixed + variable + buffer,
    breakdown: { Fixed: fixed, Variable: variable, Buffer: buffer },
  };
}

/**
 * UI component – shows total and optional breakdown.
 *
 * Props
 * -----
 * items            – array of budget items (value + optional multiplier)
 * onEstimateChange – callback(total) – called after each recompute
 * showBreakdown    – boolean (default: false) – render the three‑part breakdown
 */
export default function CostEstimates({
  items,
  onEstimateChange,
  showBreakdown = false,
}) {
  const [{ total, breakdown }, setState] = useState(() =>
    calculateEstimate(items)
  );

  // Re‑calculate whenever the items array changes
  useEffect(() => {
    const result = calculateEstimate(items);
    setState(result);
    if (typeof onEstimateChange === "function") {
      onEstimateChange(result.total);
    }
  }, [items, onEstimateChange]);

  return (
    <div className="cost-estimates" aria-live="polite">
      <h3>Cost Estimate</h3>
      <p data-testid="cost-estimate">${total.toFixed(2)}</p>

      {showBreakdown && (
        <table className="breakdown-table" data-testid="breakdown-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>Amount ($)</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(breakdown).map(([k, v]) => (
              <tr key={k}>
                <td>{k}</td>
                <td>{v.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

CostEstimates.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
        .isRequired,
      multiplier: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    })
  ).isRequired,
  onEstimateChange: PropTypes.func,
  showBreakdown: PropTypes.bool,
};

CostEstimates.defaultProps = {
  onEstimateChange: null,
  showBreakdown: false,
};