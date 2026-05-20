import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css";               // existing styles

/* -----------------------------------------------------------------------
 * Mock hook – in real code this would call an API / context.
 * Keeping it here makes the component runnable out‑of‑the‑box.
 * --------------------------------------------------------------------- */
export function useBulkCredits() {
  // Replace with real implementation later.
  return { remaining: 0, total: 0 };
}

/* -----------------------------------------------------------------------
 * BulkCreditAlert
 *
 * Props:
 *   - remaining (number) – credits left
 *   - total     (number) – total purchased credits
 *
 * Behaviour:
 *   • Visible only when total > 0 && remaining/total ≤ 0.15
 *   • Dismiss button stores a flag in localStorage (key: "bulkAlertDismissed")
 *   • On mount the component reads that flag; if the low‑credit condition
 *     still holds the banner is shown again.
 * --------------------------------------------------------------------- */
function BulkCreditAlert({ remaining, total }) {
  const [visible, setVisible] = useState(false);
  const STORAGE_KEY = "bulkAlertDismissed";

  // Decide whether the banner should be shown.
  useEffect(() => {
    if (total === 0) {
      setVisible(false);
      return;
    }

    const lowCredits = remaining / total <= 0.15;
    const dismissed = localStorage.getItem(STORAGE_KEY) === "true";

    setVisible(lowCredits && !dismissed);
  }, [remaining, total]);

  // Persist dismissal and hide banner.
  const handleDismiss = () => {
    localStorage.setItem(STORAGE_KEY, "true");
    setVisible(false);
  };

  if (!visible) return null;

  const percent = Math.round((remaining / total) * 100);

  return (
    <div className="bulk-credit-alert banner" data-testid="bulk-alert-banner">
      <span>
        Bulk credits are low ({percent}% remaining – {remaining} of {total}).
      </span>

      <Link to="/bulk-purchase" className="cta-button bulk-alert-cta">
        Purchase More
      </Link>

      <button
        className="dismiss-button bulk-alert-dismiss"
        onClick={handleDismiss}
        aria-label="Dismiss alert"
      >
        ×
      </button>
    </div>
  );
}

/* -----------------------------------------------------------------------
 * Dashboard – the page that the user lands on.
 *
 * Accepts an optional `bulkData` prop so tests (or other callers) can inject
 * deterministic values without having to mock the hook.
 * --------------------------------------------------------------------- */
export default function Dashboard({ bulkData }) {
  const hookData = useBulkCredits();
  const { remaining, total } = bulkData ?? hookData;

  return (
    <div className="dashboard-page">
      <BulkCreditAlert remaining={remaining} total={total} />
      {/* -----------------------------------------------------------------
       * Existing dashboard UI goes here.
       * ----------------------------------------------------------------- */}
      <h1>Dashboard</h1>
      {/* …other components… */}
    </div>
  );
}