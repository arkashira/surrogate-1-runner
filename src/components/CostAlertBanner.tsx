import React, { useEffect, useState } from 'react';
import { ALERT_TIMEOUT_MS } from '../config';
import './CostAlertBanner.css'; // optional – add your own styles

interface CostAlertBannerProps {
  commitSha: string;
  cost: number;
  onDismiss: () => void;
}

/**
 * A banner that notifies the user when a commit exceeds a cost threshold.
 * - Auto‑hides after ALERT_TIMEOUT_MS.
 * - Can be manually dismissed.
 * - Fully typed and unit‑tested.
 */
export const CostAlertBanner: React.FC<CostAlertBannerProps> = ({
  commitSha,
  cost,
  onDismiss,
}) => {
  const [isVisible, setIsVisible] = useState(true);

  // Auto‑hide after the configured timeout
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(false), ALERT_TIMEOUT_MS);
    return () => clearTimeout(timer);
  }, []);

  if (!isVisible) return null;

  return (
    <section className="cost-alert-banner" role="alert" aria-live="assertive">
      <div className="cost-alert-banner__content">
        <span>
          Commit <strong>{commitSha}</strong> exceeded cost threshold:{' '}
          <strong>${cost.toFixed(2)}</strong>
        </span>
        <a
          href={`/surrogate-1/api/cost-details?commit=${encodeURIComponent(
            commitSha,
          )}`}
          className="cost-alert-banner__link"
        >
          View Details
        </a>
        <button
          type="button"
          className="cost-alert-banner__dismiss"
          onClick={onDismiss}
        >
          Dismiss
        </button>
      </div>
    </section>
  );
};

export default CostAlertBanner;