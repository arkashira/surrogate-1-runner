import React, { useState, useEffect } from "react";
import CostEstimates, { calculateEstimates } from "./CostEstimates";
import "./BudgetOptimization.css";

/**
 * Generates human‑readable suggestions based on the current budget
 * and the cost‑model outcome.
 *
 * @param {number} budget – User entered budget.
 * @param {{total:number}} estimates – Result of calculateEstimates().
 * @returns {string[]} Array of suggestion strings.
 */
export const generateSuggestions = (budget, estimates) => {
  const suggestions = [];

  // 1️⃣ Budget vs. total cost
  if (estimates.total > budget) {
    suggestions.push("Your projected total exceeds the budget – consider trimming variable expenses.");
  } else {
    suggestions.push("Great! Your projected total is within the budget.");
  }

  // 2️⃣ Size‑based advice
  if (budget === 0) {
    suggestions.push("Enter a budget to receive suggestions.");
    return suggestions;
  }

  if (budget < 500) {
    suggestions.push("A modest budget – focus on essential items and keep a small emergency buffer.");
  } else if (budget <= 1500) {
    suggestions.push("Solid mid‑range budget – look for discounts on recurring services.");
  } else {
    suggestions.push("Large budget – explore bulk‑purchase discounts and negotiate contracts.");
  }

  // 3️⃣ Emergency fund recommendation (10 % of budget)
  suggestions.push(`Consider setting aside at least 10 % ($${(budget * 0.1).toFixed(2)}) as an emergency fund.`);

  return suggestions;
};

const BudgetOptimization = () => {
  const [budget, setBudget] = useState(0);
  const [suggestions, setSuggestions] = useState([]);

  // Re‑calculate suggestions whenever the budget changes
  useEffect(() => {
    const estimates = calculateEstimates(budget);
    setSuggestions(generateSuggestions(budget, estimates));
  }, [budget]);

  const handleBudgetChange = (e) => {
    const value = Number(e.target.value);
    setBudget(isNaN(value) || value < 0 ? 0 : value);
  };

  return (
    <div className="budget-optimization-page">
      <h2>Budget Optimization</h2>

      <div className="budget-input">
        <label htmlFor="budget-input">Enter your monthly budget ($):</label>
        <input
          id="budget-input"
          type="number"
          min="0"
          value={budget}
          onChange={handleBudgetChange}
          placeholder="e.g., 1500"
        />
      </div>

      {/* Cost estimate UI */}
      <CostEstimates budget={budget} />

      {/* Suggestions UI */}
      <section className="suggestions">
        <h3>Suggestions</h3>
        <ul>
          {suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default BudgetOptimization;