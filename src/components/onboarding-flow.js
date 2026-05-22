import React, { useState } from "react";
import "./onboarding-flow.css";

/**
 * OnboardingFlow
 *
 * @param {{ onFinish: () => void }} props
 *   onFinish – called when the user clicks the final CTA (e.g. start first run)
 *
 * The flow is completely driven by the `steps` array below.  Each step may
 * optionally define a `cta` label; when present the button triggers `onFinish`
 * instead of moving to the next step.
 */
export default function OnboardingFlow({ onFinish }) {
  // -------------------------------------------------------------------------
  // 1️⃣  Step definitions – edit/extend here
  // -------------------------------------------------------------------------
  const steps = [
    {
      title: "Welcome to Surrogate‑1",
      content:
        "Surrogate‑1 helps you ingest and process public datasets at scale. " +
        "This short onboarding will get you up and running in under 10 minutes.",
    },
    {
      title: "Quick Tour",
      content:
        "• Parallel runners run every 30 min\n" +
        "• Each runner processes a deterministic slice of the dataset\n" +
        "• Results are automatically uploaded to the HuggingFace hub",
    },
    {
      title: "Connect Your Data",
      content:
        "Link your data sources (CSV, JSON, Parquet, …) and let Surrogate‑1 handle the rest.",
    },
    {
      title: "Configure Processing",
      content:
        "Set up your processing parameters with our intuitive UI – no code required.",
    },
    {
      title: "Your First Action",
      content:
        "Launch your first ingestion run now. Click the button below to start processing.",
      cta: "Start First Run",
    },
  ];

  // -------------------------------------------------------------------------
  // 2️⃣  Local UI state
  // -------------------------------------------------------------------------
  const [current, setCurrent] = useState(0);
  const [completed, setCompleted] = useState(false);

  const isLastStep = current === steps.length - 1;
  const { title, content, cta } = steps[current];

  // -------------------------------------------------------------------------
  // 3️⃣  Handlers
  // -------------------------------------------------------------------------
  const goNext = () => {
    if (!isLastStep) setCurrent(current + 1);
    else setCompleted(true);
  };

  const goPrev = () => {
    if (current > 0) setCurrent(current - 1);
  };

  const handleCta = () => {
    if (onFinish) onFinish();
    // Reset flow so the user can start another run if they wish
    setCurrent(0);
    setCompleted(false);
  };

  // -------------------------------------------------------------------------
  // 4️⃣  Render
  // -------------------------------------------------------------------------
  if (completed) {
    return (
      <div className="onboarding-container completed">
        <h2>All Set! 🎉</h2>
        <p>You’ve finished the walkthrough. Ready to create your first project?</p>
        <button className="cta-button" onClick={handleCta}>
          {steps[steps.length - 1].cta || "Start"}
        </button>
      </div>
    );
  }

  return (
    <div className="onboarding-container">
      {/* Progress bar */}
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${((current + 1) / steps.length) * 100}%` }}
        />
      </div>

      {/* Dot indicator (mirrors the bar) */}
      <div className="dot-indicator">
        {steps.map((_, i) => (
          <span
            key={i}
            className={`dot ${i === current ? "active" : ""}`}
          />
        ))}
      </div>

      {/* Step content */}
      <div className="step-content">
        <h2>{title}</h2>
        <p>{content.split("\n").map((line, i) => (
          // Preserve line‑breaks from bullet lists
          <React.Fragment key={i}>
            {line}
            <br />
          </React.Fragment>
        ))}</p>
      </div>

      {/* Navigation */}
      <div className="navigation">
        <button
          className="nav-button"
          onClick={goPrev}
          disabled={current === 0}
        >
          Previous
        </button>

        {cta ? (
          <button className="nav-button primary cta" onClick={handleCta}>
            {cta}
          </button>
        ) : (
          <button className="nav-button primary" onClick={goNext}>
            {isLastStep ? "Complete" : "Next"}
          </button>
        )}
      </div>
    </div>
  );
}