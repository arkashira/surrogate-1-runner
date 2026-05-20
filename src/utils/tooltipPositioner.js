/**
 * Calculate a tooltip position for a given preferred side.
 * Returns { top, left } in viewport coordinates.
 */
export const calculateTooltipPosition = (
  triggerRect,
  tooltipRect,
  preferred = 'top',
  offset = 8
) => {
  const positions = {
    top: {
      top: triggerRect.top - tooltipRect.height - offset,
      left: triggerRect.left + (triggerRect.width - tooltipRect.width) / 2,
    },
    bottom: {
      top: triggerRect.bottom + offset,
      left: triggerRect.left + (triggerRect.width - tooltipRect.width) / 2,
    },
    left: {
      top: triggerRect.top + (triggerRect.height - tooltipRect.height) / 2,
      left: triggerRect.left - tooltipRect.width - offset,
    },
    right: {
      top: triggerRect.top + (triggerRect.height - tooltipRect.height) / 2,
      left: triggerRect.right + offset,
    },
  };

  // Start with the preferred side
  let { top, left } = positions[preferred] ?? positions.top;

  // ---- Boundary correction (horizontal) ----
  const viewportWidth = window.innerWidth;
  if (left < 0) left = 8; // keep a small gutter
  if (left + tooltipRect.width > viewportWidth)
    left = viewportWidth - tooltipRect.width - 8;

  // ---- Boundary correction (vertical) ----
  const viewportHeight = window.innerHeight;
  if (top < 0) top = triggerRect.bottom + offset; // flip to bottom if off‑top
  if (top + tooltipRect.height > viewportHeight)
    top = triggerRect.top - tooltipRect.height - offset; // flip to top if off‑bottom

  return { top, left };
};

/**
 * Choose the first position from `candidates` that fits without clipping.
 * If none fit, fall back to the first candidate (with boundary correction).
 */
export const getOptimalPosition = (
  triggerRect,
  tooltipRect,
  candidates = ['top', 'bottom', 'right', 'left'],
  offset = 8
) => {
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  const fits = (pos) => {
    const { top, left } = calculateTooltipPosition(
      triggerRect,
      tooltipRect,
      pos,
      offset
    );
    return (
      top >= 0 &&
      left >= 0 &&
      top + tooltipRect.height <= viewportHeight &&
      left + tooltipRect.width <= viewportWidth
    );
  };

  const chosen = candidates.find(fits) ?? candidates[0];
  return calculateTooltipPosition(triggerRect, tooltipRect, chosen, offset);
};