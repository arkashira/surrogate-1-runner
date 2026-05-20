/**
 * Calculates a potential score for a startup idea.
 *
 * The algorithm:
 *  1. Normalizes every metric to [0, 1] (capped at 1).
 *  2. Multiplies each metric by a weight.
 *  3. Sums the weighted values → final potential (0‑1).
 *  4. Maps the numeric potential to a human‑readable bucket.
 *
 * The design is intentionally lightweight so that users can tweak
 * weights or add new metrics without touching the core logic.
 */

export interface IdeaMetrics {
  /** Total Addressable Market in millions USD (0‑∞) */
  marketSize: number;
  /** Competition intensity (0 = no competition, 1 = saturated market) */
  competition: number;
  /** Average years of relevant experience of the founding team */
  teamExperience: number;
  /** Projected growth potential (0‑∞) */
  growthPotential: number;
  /** Strength of the revenue model (0‑∞) */
  revenueModel: number;
  /** Level of customer validation (0‑∞) */
  customerValidation: number;
}

/**
 * Normalizes a numeric value to the range [0, 1] based on an expected maximum.
 * If the value exceeds the maximum, it is capped at 1.
 *
 * @param value - Raw metric value.
 * @param max   - Expected maximum for that metric.
 * @returns Normalized value between 0 and 1.
 */
function normalize(value: number, max: number): number {
  if (max <= 0) return 0;
  const n = value / max;
  return Math.min(Math.max(n, 0), 1);
}

/**
 * The core calculator.
 *
 * - `WEIGHTS` can be tweaked or extended.
 * - `MAX_VALUES` defines the expected maximum for each metric.
 *   These are used only for normalization; they do **not** affect the
 *   relative importance of the metrics.
 */
export class PotentialCalculator {
  /** Relative importance of each metric. */
  private static readonly WEIGHTS: Record<keyof IdeaMetrics, number> = {
    marketSize: 0.30,
    competition: 0.20,
    teamExperience: 0.15,
    growthPotential: 0.20,
    revenueModel: 0.10,
    customerValidation: 0.05,
  };

  /** Expected maximum values for normalization. */
  private static readonly MAX_VALUES: Record<keyof IdeaMetrics, number> = {
    marketSize: 1000,          // $1B TAM
    competition: 1,            // already 0‑1
    teamExperience: 20,        // 20 years
    growthPotential: 10,       // arbitrary scale 0‑10
    revenueModel: 10,          // arbitrary scale 0‑10
    customerValidation: 10,    // arbitrary scale 0‑10
  };

  /**
   * Calculates a raw potential score (0‑1).
   *
   * @param metrics - The metrics for a startup idea.
   * @returns Normalized potential score.
   */
  calculatePotential(metrics: IdeaMetrics): number {
    let potential = 0;

    for (const key of Object.keys(PotentialCalculator.WEIGHTS) as (keyof IdeaMetrics)[]) {
      const raw = metrics[key];
      const max = PotentialCalculator.MAX_VALUES[key];
      const weight = PotentialCalculator.WEIGHTS[key];
      const normalized = normalize(raw, max);
      potential += normalized * weight;
    }

    // Clamp to [0, 1] just in case rounding errors creep in.
    return Math.min(Math.max(potential, 0), 1);
  }

  /**
   * Maps a numeric potential to a human‑readable bucket.
   *
   * @param potential - The raw potential (0‑1).
   * @returns One of: “High Potential”, “Moderate Potential”, “Low Potential”, “Very Low Potential”.
   */
  getPotentialScore(potential: number): string {
    if (potential >= 0.80) return "High Potential";
    if (potential >= 0.60) return "Moderate Potential";
    if (potential >= 0.40) return "Low Potential";
    return "Very Low Potential";
  }
}