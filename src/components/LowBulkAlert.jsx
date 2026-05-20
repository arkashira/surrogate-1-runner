import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

/**
 * LowBulkAlert
 *
 * Props
 * ------
 * - **remaining** (number) – current bulk‑credit balance.
 * - **total** (number) – total bulk‑credit allocation.
 *
 * Behaviour
 * ---------
 * 1. Shows a banner when `remaining / total <= 0.15` (≤ 15 % left).
 * 2. The banner can be dismissed. Dismissal is stored in `localStorage`
 *    under the key `lowBulkAlertDismissed`.
 * 3. The dismissal **only lasts for the current page load** – on the next
 *    navigation or refresh the component re‑evaluates the low‑bulk condition
 *    and, if still true, shows the banner again.  
 *    (We achieve this by **clearing the flag on every mount** before we read it.)
 * 4. The component is fully typed with PropTypes and includes ARIA labels for
 *    screen‑reader friendliness.
 */
export default function LowBulkAlert({ remaining, total }) {
  const STORAGE_KEY = "lowBulkAlertDismissed";

  const [visible, setVisible] = useState(false);

  // 1️⃣ Low‑bulk condition (guard against division by zero)
  const isLow = total > 0 && remaining / total <= 0.15;

  // 2️⃣ On every mount we *reset* any stale dismissal flag.
  //    This satisfies the “re‑appear on next load if condition persists” rule.
  useEffect(() => {
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  // 3️⃣ Decide whether to show the banner.
  //    We read the flag **after** the reset so a fresh load always starts clean.
  useEffect(() => {
    if (!isLow) {
      setVisible(false);
      return;
    }

    const dismissed = localStorage.getItem(STORAGE_KEY) === "true";
    setVisible(!dismissed);
  }, [isLow]);

  // 4️⃣ Dismiss handler – hides banner and persists the flag for the *current* session.
  const handleDismiss = () => {
    localStorage.setItem(STORAGE_KEY, "true");
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div
      data-testid="low-bulk-alert"
      role="alert"
      style={{
        backgroundColor: "#fff3cd",
        color: "#856404",
        padding: "12px 24px",
        borderBottom: "1px solid #ffeeba",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <span>
        ⚠️ Bulk credits are low ({remaining} remaining of {total}). Please
        purchase more to avoid downtime.
      </span>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        <a
          href="/purchase-bulk-credits"
          data-testid="low-bulk-cta"
          style={{
            backgroundColor: "#004085",
            color: "#fff",
            padding: "6px 12px",
            borderRadius: "4px",
            textDecoration: "none",
          }}
        >
          Purchase Credits
        </a>

        <button
          onClick={handleDismiss}
          aria-label="Dismiss low‑bulk alert"
          data-testid="low-bulk-dismiss"
          style={{
            background: "transparent",
            border: "none",
            fontSize: "16px",
            cursor: "pointer",
            color: "#856404",
          }}
        >
          ✕
        </button>
      </div>
    </div>
  );
}

/* ---------- PropTypes (runtime type‑checking) ---------- */
LowBulkAlert.propTypes = {
  /** Remaining bulk credits */
  remaining: PropTypes.number.isRequired,
  /** Total bulk credits allocated */
  total: PropTypes.number.isRequired,
};