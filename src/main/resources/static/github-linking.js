/**
 * GitHub Issue and Pull Request Linking Utility
 *
 * This module scans the current page for Markdown links that reference
 * GitHub issue or pull request URLs and replaces them with
 * a more user-friendly preview link that opens in a new tab.
 *
 * It also detects standalone issue numbers and PR references in the text
 * and converts them into clickable links.
 *
 * Usage:
 *   1. Include this script in the HTML of the knowledge article page.
 *   2. The script will automatically transform links like:
 *      https://github.com/owner/repo/issues/123
 *      https://github.com/owner/repo/pull/456
 *   3. The transformed link will display as:
 *      #123 (Issue) or #456 (Pull Request)
 *
 * Note: This script assumes that the page contains a container with the
 * class `markdown-body` (the default class used by GitHub's Markdown preview).
 */

(function () {
  const GITHUB_ISSUE_REGEX = /https?:\/\/github\.com\/([^/]+)\/([^/]+)\/issues\/(\d+)/i;
  const GITHUB_PR_REGEX = /https?:\/\/github\.com\/([^/]+)\/([^/]+)\/pull\/(\d+)/i;
  const ISSUE_NUMBER_REGEX = /#(\d+)/g;
  const PR_REFERENCE_REGEX = /\\bPR:\\s*#?(\d+)\\b/g;

  /**
   * Transform a single anchor element if it matches a GitHub issue or PR.
   * @param {HTMLAnchorElement} link
   */
  function transformLink(link) {
    const href = link.getAttribute('href');
    if (!href) return;

    let match = GITHUB_ISSUE_REGEX.exec(href);
    if (match) {
      const [, owner, repo, issueNumber] = match;
      link.textContent = `#${issueNumber} (Issue)`;
      link.setAttribute('title', `View issue #${issueNumber} on ${owner}/${repo}`);
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
      return;
    }

    match = GITHUB_PR_REGEX.exec(href);
    if (match) {
      const [, owner, repo, prNumber] = match;
      link.textContent = `#${prNumber} (Pull Request)`;
      link.setAttribute('title', `View PR #${prNumber} on ${owner}/${repo}`);
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  }

  /**
   * Scan the document for Markdown links and transform them.
   */
  function init() {
    // GitHub's Markdown preview container
    const container = document.querySelector('.markdown-body');
    if (!container) return;

    const links = container.querySelectorAll('a[href]');
    links.forEach(transformLink);

    // Process text to replace issue numbers and PR references
    const text = container.textContent;
    const processedText = processGitHubLinks(text);
    container.innerHTML = processedText;
  }

  /**
   * Processes text to replace GitHub issue and pull request references with hyperlinks.
   * @param {string} text
   * @returns {string} processed text with issue numbers and PR references converted to links
   */
  function processGitHubLinks(text) {
    // Replace issue numbers
    text = text.replace(ISSUE_NUMBER_REGEX, (match, number) => {
      return `<a href="https://github.com/axentx/knowledge-radar/issues/${number}" target="_blank">${match}</a>`;
    });

    // Replace PR references
    text = text.replace(PR_REFERENCE_REGEX, (match, number) => {
      return `<a href="https://github.com/axentx/knowledge-radar/pull/${number}" target="_blank">${match}</a>`;
    });

    return text;
  }

  // Run after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();