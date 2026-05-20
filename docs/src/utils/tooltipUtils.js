const TOOLTIP_KEY = 'dismissedTooltips';

/**
 * Returns true if the tooltip for `featureId` has NOT been dismissed.
 */
export function shouldShowTooltip(featureId) {
  const dismissed = JSON.parse(sessionStorage.getItem(TOOLTIP_KEY) || '[]');
  return !dismissed.includes(featureId);
}

/**
 * Marks a tooltip as dismissed.
 */
export function dismissTooltip(featureId) {
  const dismissed = JSON.parse(sessionStorage.getItem(TOOLTIP_KEY) || '[]');
  if (!dismissed.includes(featureId)) {
    dismissed.push(featureId);
    sessionStorage.setItem(TOOLTIP_KEY, JSON.stringify(dismissed));
  }
}

/**
 * Opens the documentation page for a feature.
 * In a real app this could open a modal or navigate.
 */
export function openHelp(featureId, docs) {
  const doc = docs[featureId];
  if (doc) {
    // Example: navigate to the link
    window.location.href = doc.link;
  }
}