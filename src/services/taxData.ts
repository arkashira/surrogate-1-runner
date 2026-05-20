export interface TaxBracket {
  /** Human‑readable label, e.g. “22%” */
  label: string;
  /** Lower bound (inclusive) of taxable income for this bracket */
  min: number;
  /** Upper bound (exclusive) of taxable income for this bracket */
  max: number;
  /** The marginal rate expressed as a decimal (0.22 for 22 %) */
  rate: number;
}

/**
 * Example data – replace with the official IRS tables.
 */
export const TAX_BRACKETS: TaxBracket[] = [
  { label: '10%', min: 0,        max: 10_275,   rate: 0.10 },
  { label: '12%', min: 10_275,   max: 41_775,   rate: 0.12 },
  { label: '22%', min: 41_775,   max: 89_075,   rate: 0.22 },
  { label: '24%', min: 89_075,   max: 170_050,  rate: 0.24 },
  { label: '32%', min: 170_050,  max: 215_950,  rate: 0.32 },
  { label: '35%', min: 215_950,  max: 539_900,  rate: 0.35 },
  { label: '37%', min: 539_900,  max: Infinity, rate: 0.37 },
];