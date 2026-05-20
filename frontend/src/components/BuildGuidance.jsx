import React, { useState } from "react";
import Recommendations from "./Recommendations";

/**
 * BuildGuidance
 *
 * Renders controls for:
 *   • Budget – a slider (500‑5000, step 50) that displays the current value.
 *   • Primary needs – a set of check‑boxes (gaming, video editing, workstation).
 *
 * The selected values are passed to <Recommendations/> which updates in real‑time.
 */
export default function BuildGuidance() {
  // ---- State --------------------------------------------------------------
  const [budget, setBudget] = useState(1500);
  const [needs, setNeeds] = useState({
    gaming: false,
    videoEditing: false,
    workstation: false,
  });

  // ---- Handlers ------------------------------------------------------------
  const handleBudgetChange = (e) => setBudget(Number(e.target.value));

  const toggleNeed = (needKey) =>
    setNeeds((prev) => ({ ...prev, [needKey]: !prev[needKey] }));

  // ---- Render --------------------------------------------------------------
  return (
    <section className="build-guidance">
      <h2>Build Guidance</h2>

      {/* ---------- Budget Slider ---------- */}
      <div className="input-section">
        <label htmlFor="budget-range">
          Budget: <strong>${budget}</strong>
        </label>
        <input
          id="budget-range"
          type="range"
          min="500"
          max="5000"
          step="50"
          value={budget}
          onChange={handleBudgetChange}
        />
      </div>

      {/* ---------- Needs Check‑boxes ---------- */}
      <fieldset className="needs-fieldset">
        <legend>Select your primary needs</legend>
        {Object.keys(needs).map((key) => (
          <label key={key} style={{ marginRight: "1rem" }}>
            <input
              type="checkbox"
              checked={needs[key]}
              onChange={() => toggleNeed(key)}
            />
            {key === "videoEditing"
              ? "Video Editing"
              : key.charAt(0).toUpperCase() + key.slice(1)}
          </label>
        ))}
      </fieldset>

      {/* ---------- Recommendations ---------- */}
      <Recommendations budget={budget} needs={needs} />
    </section>
  );
}