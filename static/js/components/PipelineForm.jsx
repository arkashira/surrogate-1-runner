import React, { useState } from "react";

/**
 * PipelineForm
 *
 * Props
 * -----
 * onSave(pipeline) – called with the newly created pipeline object.
 *
 * Pipeline shape
 * --------------
 * {
 *   id: string,            // UUID
 *   name: string,          // ≤ 50 chars
 *   stages: string[]       // unique, non‑empty
 * }
 *
 * Validation rules
 * ----------------
 * • name required, max 50 characters
 * • at least 3 stages
 * • stage names must be non‑empty and unique
 */
export default function PipelineForm({ onSave }) {
  const [name, setName] = useState("");
  const [stages, setStages] = useState(["", "", ""]); // start with three blanks
  const [errors, setErrors] = useState({});

  // -----------------------------------------------------------------
  // Helpers
  // -----------------------------------------------------------------
  const handleStageChange = (idx, value) => {
    const copy = [...stages];
    copy[idx] = value;
    setStages(copy);
  };

  const addStage = () => setStages([...stages, ""]);

  const validate = () => {
    const errs = {};

    // ---- name -------------------------------------------------------
    const trimmedName = name.trim();
    if (!trimmedName) {
      errs.name = "Pipeline name is required.";
    } else if (trimmedName.length > 50) {
      errs.name = "Name must be 50 characters or fewer.";
    }

    // ---- stages ------------------------------------------------------
    const trimmedStages = stages.map((s) => s.trim()).filter(Boolean);
    if (trimmedStages.length < 3) {
      errs.stages = "At least three stages are required.";
    } else {
      const dupes = trimmedStages.filter(
        (s, i) => trimmedStages.indexOf(s) !== i
      );
      if (dupes.length) {
        errs.stages = "Stage names must be unique.";
      }
    }

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  // -----------------------------------------------------------------
  // Submit
  // -----------------------------------------------------------------
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    const pipeline = {
      id: crypto.randomUUID(),
      name: name.trim(),
      stages: stages.map((s) => s.trim()).filter(Boolean),
    };

    onSave(pipeline);

    // reset UI
    setName("");
    setStages(["", "", ""]);
    setErrors({});
  };

  // -----------------------------------------------------------------
  // Render
  // -----------------------------------------------------------------
  return (
    <form onSubmit={handleSubmit} className="pipeline-form">
      <h2>Create New Pipeline</h2>

      {/* ---- name --------------------------------------------------- */}
      <div>
        <label>
          Pipeline Name:
          <input
            type="text"
            value={name}
            maxLength={50}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Order Fulfilment"
          />
        </label>
        {errors.name && <div className="error">{errors.name}</div>}
      </div>

      {/* ---- stages ------------------------------------------------- */}
      <div className="stages-block">
        <label>Stages:</label>
        {stages.map((stage, idx) => (
          <div key={idx} className="stage-input">
            <input
              type="text"
              placeholder={`Stage ${idx + 1}`}
              value={stage}
              onChange={(e) => handleStageChange(idx, e.target.value)}
            />
          </div>
        ))}
        {errors.stages && <div className="error">{errors.stages}</div>}
        <button type="button" onClick={addStage} className="add-stage">
          + Add Stage
        </button>
      </div>

      <button type="submit" className="save-btn">
        Save Pipeline
      </button>
    </form>
  );
}