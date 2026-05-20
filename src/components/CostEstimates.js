import React from "react";
import PropTypes from "prop-types";
import "./CostEstimates.css";

/**
 * Simple deterministic cost model.
 *
 * @param {number} budget – The user‑provided budget.
 * @param {{base:number, variable:number}} [factors] – Multipliers for the two cost legs.
 * @returns {{baseCost:number, variableCost:number, total:number}}
 */
export const calculateEstimates = (budget, factors = { base: 1.2, variable: 0.8 }) => {
  const baseCost = budget * factors.base;
  const variableCost = budget * factors.variable;
  const total = baseCost + variableCost;

  // Round to two decimal places for UI friendliness
  const round = (n) => Math.round(n * 100) / 100;

  return {
    baseCost: round(baseCost),
    variableCost: round(variableCost),
    total: round(total),
  };
};

/**
 * Presentation component – shows the three cost numbers.
 *
 * @param {{budget:number}} props
 */
const CostEstimates = ({ budget }) => {
  const { baseCost, variableCost, total } = calculateEstimates(budget);

  return (
    <div className="cost-estimates">
      <h3>Cost Estimates</h3>
      <ul>
        <li>Base Cost: <strong>${baseCost.toLocaleString()}</strong></li>
        <li>Variable Cost: <strong>${variableCost.toLocaleString()}</strong></li>
        <li>Total: <strong>${total.toLocaleString()}</strong></li>
      </ul>
    </div>
  );
};

CostEstimates.propTypes = {
  /** Budget entered by the user (must be a non‑negative number) */
  budget: PropTypes.number.isRequired,
};

export default CostEstimates;