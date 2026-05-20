const fs = require('fs');
const path = require('path');

/**
 * Directory where generated reports are stored.
 * It will be created on first use if it does not exist.
 */
const REPORTS_DIR = path.resolve(__dirname, 'output');

/**
 * Mock function to retrieve a user's language‑learning progress.
 * In a real system this would query a database or an external service.
 *
 * @param {string} userId
 * @returns {Promise<Object>} progress data
 */
async function fetchUserProgress(userId) {
  // Simulated data – replace with real data source later.
  return {
    userId,
    totalWordsLearned: 1245,
    dailyStreak: 9, // consecutive days
    lastSevenDays: [
      { date: '2026-05-09', wordsLearned: 30 },
      { date: '2026-05-10', wordsLearned: 45 },
      { date: '2026-05-11', wordsLearned: 20 },
      { date: '2026-05-12', wordsLearned: 0 },
      { date: '2026-05-13', wordsLearned: 15 },
      { date: '2026-05-14', wordsLearned: 25 },
      { date: '2026-05-15', wordsLearned: 40 },
    ],
  };
}

/**
 * Derive actionable insights from progress data.
 *
 * @param {Object} data
 * @returns {string[]} array of insight sentences
 */
function generateInsights(data) {
  const insights = [];

  // Insight about streak
  if (data.dailyStreak >= 7) {
    insights.push(
      `🎉 Great job! You’ve kept a ${data.dailyStreak}-day streak. Keep the momentum!`
    );
  } else if (data.dailyStreak > 0) {
    insights.push(
      `👍 You’re on a ${data.dailyStreak}-day streak. Try to reach 7 days for a bonus reward.`
    );
  } else {
    insights.push(`🚀 Let’s start a learning streak today!`);
  }

  // Insight about recent activity
  const recentTotal = data.lastSevenDays.reduce(
    (sum, d) => sum + d.wordsLearned,
    0
  );
  const avgPerDay = Math.round(recentTotal / 7);
  insights.push(
    `📈 In the last 7 days you learned ${recentTotal} words (≈${avgPerDay} per day).`
  );

  // Suggestion if activity dropped
  const yesterday = data.lastSevenDays[data.lastSevenDays.length - 2];
  const today = data.lastSevenDays[data.lastSevenDays.length - 1];
  if (today.wordsLearned < yesterday.wordsLearned) {
    insights.push(
      `🔔 You learned fewer words today than yesterday. Consider a short review session.`
    );
  }

  return insights;
}

/**
 * Render a markdown report from progress data and insights.
 *
 * @param {Object} data
 * @param {string[]} insights
 * @returns {string} markdown content
 */
function renderMarkdownReport(data, insights) {
  const lines = [];

  lines.push(`# Language Learning Progress Report`);
  lines.push(`**User:** ${data.userId}`);
  lines.push(`**Generated:** ${new Date().toISOString()}`);
  lines.push(`---`);
  lines.push(`## Summary`);
  lines.push(`- Total words learned: **${data.totalWordsLearned}**`);
  lines.push(`- Current daily streak: **${data.dailyStreak}** days`);
  lines.push(`---`);
  lines.push(`## Recent Activity (last 7 days)`);
  lines.push(`| Date | Words Learned |`);
  lines.push(`|------|---------------|`);
  data.lastSevenDays.forEach((d) => {
    lines.push(`| ${d.date} | ${d.wordsLearned} |`);
  });
  lines.push(`---`);
  lines.push(`## Actionable Insights`);
  insights.forEach((ins) => lines.push(`- ${ins}`));

  return lines.join('\n');
}

/**
 * Ensure the reports output directory exists.
 */
function ensureReportsDir() {
  if (!fs.existsSync(REPORTS_DIR)) {
    fs.mkdirSync(REPORTS_DIR, { recursive: true });
  }
}

/**
 * Save the markdown report to a file.
 *
 * @param {string} userId
 * @param {string} content markdown content
 * @returns {string} absolute path of the written file
 */
function saveReport(userId, content) {
  ensureReportsDir();
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `${userId}-${timestamp}.md`;
  const filePath = path.join(REPORTS_DIR, filename);
  fs.writeFileSync(filePath, content, 'utf8');
  return filePath;
}

/**
 * Public API – generate a report for a given user and return the file path.
 *
 * @param {string} userId
 * @returns {Promise<string>} absolute path to the generated report
 */
async function generateReport(userId) {
  const data = await fetchUserProgress(userId);
  const insights = generateInsights(data);
  const markdown = renderMarkdownReport(data, insights);
  return saveReport(userId, markdown);
}

/**
 * Optional helper to schedule daily report generation for a list of users.
 * Uses `node-cron` if available; otherwise it’s a no‑op placeholder.
 *
 * @param {string[]} userIds
 */
function scheduleDailyReports(userIds) {
  try {
    const cron = require('node-cron');
    // Run every day at 02:00 AM UTC
    cron.schedule('0 2 * * *', () => {
      userIds.forEach((uid) => {
        generateReport(uid).catch((e) =>
          console.error(`Failed to generate report for ${uid}:`, e)
        );
      });
    });
  } catch (_) {
    // node-cron not installed – silently ignore; callers can invoke generateReport manually.
  }
}

module.exports = {
  generateReport,
  scheduleDailyReports, // exported for potential use elsewhere
  // Exported for unit‑testing purposes
  _private: {
    fetchUserProgress,
    generateInsights,
    renderMarkdownReport,
    saveReport,
    ensureReportsDir,
  },
};