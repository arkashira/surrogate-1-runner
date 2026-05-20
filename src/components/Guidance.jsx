import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

/**
 * Guidance tip that appears for the current onboarding task.
 *
 * @param {Object} props
 * @param {string} props.currentTask   Identifier of the active task/step.
 * @param {Object.<string,string>} props.guidanceMap  Mapping taskId → tip text.
 * @param {(taskId:string)=>void} [props.onDismiss]   Called when the user dismisses the tip.
 */
export default function Guidance({ currentTask, guidanceMap, onDismiss }) {
  const [visible, setVisible] = useState(true);
  const [lastTask, setLastTask] = useState(currentTask);

  // When the task changes we want to show the new tip again.
  useEffect(() => {
    if (currentTask !== lastTask) {
      setVisible(true);
      setLastTask(currentTask);
    }
  }, [currentTask, lastTask]);

  if (!visible) return null;

  const message = guidanceMap?.[currentTask];
  if (!message) return null; // No tip for this task.

  const handleDismiss = () => {
    setVisible(false);
    if (typeof onDismiss === "function") onDismiss(currentTask);
  };

  return (
    <div className="guidance-tip" style={styles.container} role="status" aria-live="polite">
      <div style={styles.message}>{message}</div>
      <button
        onClick={handleDismiss}
        style={styles.dismissBtn}
        aria-label="Dismiss guidance"
      >
        ✕
      </button>
    </div>
  );
}

/* ---------- PropTypes ---------- */
Guidance.propTypes = {
  currentTask: PropTypes.string.isRequired,
  guidanceMap: PropTypes.objectOf(PropTypes.string).isRequired,
  onDismiss: PropTypes.func,
};

Guidance.defaultProps = {
  onDismiss: null,
};

/* ---------- Inline style (kept simple & theme‑neutral) ---------- */
const styles = {
  container: {
    position: "relative",
    padding: "12px 16px",
    margin: "8px 0",
    backgroundColor: "#e8f4fd",
    borderRadius: "4px",
    border: "1px solid #b3d7f5",
    display: "flex",
    alignItems: "center",
    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
  },
  message: {
    flex: 1,
    fontSize: "14px",
    color: "#333",
  },
  dismissBtn: {
    background: "transparent",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
    color: "#555",
    lineHeight: 1,
  },
};