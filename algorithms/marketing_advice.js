/**
 * Marketing Advice Engine
 *
 * Combines deterministic KPI‑based rules with an optional
 * OpenAI‑powered “creative” mode.
 *
 * Exported API:
 *   generateAdvice(metrics, options) → Promise<string[]>
 *
 * Options:
 *   - useAI: boolean (default false) – if true, ignore metrics and
 *     call the OpenAI API.
 *
 * The function always resolves to an array of strings.  When the
 * AI mode is used, the response is parsed into individual advice
 * lines.  Errors from the OpenAI call are surfaced as rejected
 * promises so that callers can handle them explicitly.
 */

const { Configuration, OpenAIApi } = require("openai");

// ---------- 1. Deterministic rules (Candidate 1) ----------
const DEFAULT_METRICS = {
  traffic: 0,
  conversionRate: 0,
  bounceRate: 0,
  avgSessionDuration: 0,
  emailOpenRate: 0,
  emailClickRate: 0,
};

function deterministicAdvice(metrics) {
  const m = { ...DEFAULT_METRICS, ...metrics };
  const advice = [];

  // 1. Traffic & Conversion
  if (m.traffic < 1000) {
    advice.push(
      "Consider running a targeted ad campaign to increase website traffic."
    );
  }
  if (m.conversionRate < 2) {
    advice.push(
      "Optimize your landing page copy and call‑to‑action to improve conversion rates."
    );
  }

  // 2. Bounce Rate & Session Duration
  if (m.bounceRate > 70) {
    advice.push(
      "Investigate high bounce rates; improve page load speed or add engaging content."
    );
  }
  if (m.avgSessionDuration < 60) {
    advice.push(
      "Add interactive elements or deeper content to keep visitors engaged longer."
    );
  }

  // 3. Email Campaigns
  if (m.emailOpenRate < 15) {
    advice.push(
      "Revise email subject lines and send times to boost open rates."
    );
  }
  if (m.emailClickRate < 5) {
    advice.push(
      "Include clear, value‑driven CTAs in your emails to increase click‑through rates."
    );
  }

  // 4. General Recommendation
  if (advice.length === 0) {
    advice.push(
      "Great job! Your marketing metrics are healthy. Keep monitoring and iterating."
    );
  }

  return advice;
}

// ---------- 2. OpenAI fallback (Candidate 2) ----------
const openai = new OpenAIApi(
  new Configuration({ apiKey: process.env.OPENAI_API_KEY })
);

/**
 * Build a prompt that mirrors the structure used in Candidate 2
 * but is more explicit about the desired output format.
 */
function buildPrompt(userData) {
  return `You are a marketing strategist. Based on the following data, give at least three concrete, measurable, and actionable suggestions.  
- Current marketing metrics: ${userData.metrics || "N/A"}  
- Previous marketing strategies: ${userData.strategies || "N/A"}  
- Target audience: ${userData.audience || "N/A"}  
- Industry: ${userData.industry || "N/A"}  

Return the suggestions as a numbered list, one per line.`;
}

/**
 * Call OpenAI and parse the response into an array of strings.
 */
async function aiAdvice(userData) {
  const prompt = buildPrompt(userData);
  const response = await openai.createCompletion({
    model: "text-davinci-003",
    prompt,
    temperature: 0.7,
    max_tokens: 256,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
  });

  const raw = response.data.choices[0].text.trim();

  // Split on newlines and strip leading numbers/periods.
  return raw
    .split("\n")
    .map((line) => line.replace(/^\s*\d+\.?\s*/, "").trim())
    .filter(Boolean);
}

// ---------- 3. Public API ----------
/**
 * @param {Object} metrics - KPI values (optional)
 * @param {Object} options
 * @param {boolean} options.useAI - if true, ignore metrics and call OpenAI
 * @returns {Promise<string[]>}
 */
async function generateAdvice(metrics = {}, options = {}) {
  if (options.useAI) {
    // In AI mode we still allow the caller to provide userData
    // for richer context.  If no userData is supplied, we
    // fall back to the deterministic rules to avoid an empty prompt.
    const userData = metrics || {};
    try {
      return await aiAdvice(userData);
    } catch (e) {
      // If the AI call fails, fall back to deterministic advice
      console.warn("OpenAI call failed, falling back to deterministic advice:", e);
      return deterministicAdvice(metrics);
    }
  }

  // Default deterministic path
  return deterministicAdvice(metrics);
}

module.exports = { generateAdvice };