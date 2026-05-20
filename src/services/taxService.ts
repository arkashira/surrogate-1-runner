import { TAX_BRACKETS, TaxBracket } from './taxData';

export interface TaxInputs {
  /** After‑tax contribution to a Roth (or traditional) account */
  contributionAmount: number;
  /** Amount you plan to convert from a Traditional IRA to a Roth IRA */
  conversionAmount: number;
  /** The marginal tax rate you will pay on the conversion (as a decimal) */
  conversionTaxRate: number;
}

/** Result object that the UI will render */
export interface TaxResult {
  /** Net tax you’ll pay (or save) because of the contribution */
  taxSavingsLosses: number;
  /** Adjusted basis of the converted amount after accounting for after‑tax contributions */
  adjustedBasis: number;
  /** Additional tax impact if you later re‑characterize the conversion */
  recharacterizationImpact: number;
}

/**
 * Core algorithm – **replace the placeholder formulas with the real IRS logic**.
 *
 * The function is deliberately pure: given the same inputs it always returns the same
 * output, which makes it trivial to unit‑test.
 */
export function calculateTaxImpact({
  contributionAmount,
  conversionAmount,
  conversionTaxRate,
}: TaxInputs): TaxResult {
  // ---- 1️⃣  Contribution tax benefit (e.g., non‑deductible Roth contribution) ----
  // For a Roth contribution you get no immediate deduction, but you avoid future tax.
  // A simple placeholder: treat the contribution as a “tax saved” equal to the
  // contribution * your current marginal rate (you can look it up from TAX_BRACKETS).
  const taxSavingsLosses = contributionAmount * conversionTaxRate;

  // ---- 2️⃣  Adjusted basis of the conversion ----
  // The basis is the after‑tax dollars that have already been taxed.
  // Placeholder: contribution + (conversion – contribution) * (1 – conversionTaxRate)
  const adjustedBasis =
    contributionAmount +
    (conversionAmount - contributionAmount) * (1 - conversionTaxRate);

  // ---- 3️⃣  Recharacterization impact ----
  // If you later undo the conversion you may owe tax on the earnings portion.
  // Placeholder: earnings * conversionTaxRate
  const earnings = conversionAmount - contributionAmount;
  const recharacterizationImpact = earnings * conversionTaxRate;

  return {
    taxSavingsLosses,
    adjustedBasis,
    recharacterizationImpact,
  };
}

/**
 * Helper – find the marginal rate for a given *taxable income*.
 * This is useful if you want the UI to auto‑populate the rate based on the user’s
 * annual income instead of a manual dropdown.
 */
export function getRateForIncome(income: number): number {
  const bracket = TAX_BRACKETS.find(
    (b) => income >= b.min && income < b.max
  );
  return bracket?.rate ?? 0;
}