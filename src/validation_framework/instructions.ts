/**
 * User‑facing guidance for the Validation Framework.
 *
 * The module exports a single `instructions` object that contains
 * a flat list of sections.  Each section has:
 *
 *   • `id`      – a stable key used by the UI for routing or
 *                  accessibility.
 *   • `title`   – the heading shown in the navigation menu.
 *   • `description` – a short explanatory paragraph.
 *   • `steps`   – an ordered array of strings that can be rendered
 *                  as a numbered list.
 *
 * This structure is intentionally minimal so that it can be
 * consumed by:
 *
 *   • React/Vue components (e.g. a sidebar + content panel)
 *   • Markdown generators (e.g. `mdx` or `docz`)
 *   • Automated help‑desk widgets
 *
 * The data is fully typed, so you get compile‑time safety
 * and IDE autocomplete wherever you import it.
 */

export interface InstructionSection {
  /** Stable key – used for routing or as a React key. */
  id: string;
  /** Display name in the navigation menu. */
  title: string;
  /** One‑sentence purpose of the page. */
  description: string;
  /** Ordered list of user actions. */
  steps: string[];
}

/**
 * Ordered list of all framework sections.
 *
 * The order matches the visual order in the left‑hand navigation
 * bar: Input Form → Benchmark → Summary → Navigation help.
 */
export const instructions: InstructionSection[] = [
  {
    id: 'inputForm',
    title: 'Input Form',
    description:
      'Enter or upload the data you wish to validate. This is the starting point for all analyses.',
    steps: [
      'Navigate to the Input Form page from the navigation menu.',
      'Fill in the required fields or upload a file.',
      'Click the “Submit” button to send your data to the validation engine.',
      'Wait for the confirmation message indicating that the data has been queued.',
    ],
  },
  {
    id: 'benchmark',
    title: 'Benchmark',
    description:
      'Run performance tests on your data to assess processing speed and resource usage.',
    steps: [
      'From the navigation menu, select the Benchmark page.',
      'Choose the benchmark configuration (e.g., dataset size, concurrency).',
      'Click “Run Benchmark” to start the test.',
      'Monitor the live progress and review the final report once completed.',
    ],
  },
  {
    id: 'summary',
    title: 'Summary',
    description:
      'View the results of your validation and benchmark runs, including key metrics and recommendations.',
    steps: [
      'Select the Summary page via the navigation menu.',
      'Browse the list of recent runs and click on a run ID to see details.',
      'Review the metrics table, visualizations, and any actionable insights.',
      'Export the summary as a PDF or CSV if needed.',
    ],
  },
  {
    id: 'navigation',
    title: 'Navigation Menu',
    description:
      'The navigation menu provides quick access to all framework sections. It is located on the left side of the interface.',
    steps: [
      'Click the hamburger icon to expand the menu if it is collapsed.',
      'Select the desired section (Input Form, Benchmark, Summary).',
      'The selected section will load in the main content area.',
    ],
  },
];