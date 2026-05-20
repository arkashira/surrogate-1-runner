/**
 * Markdown Preview Utility
 *
 * A single, self‑contained script that:
 *   • Listens for `input` events on a `<textarea id="markdown-input">`
 *   • Renders the Markdown into a `<div id="markdown-output">`
 *   • Uses the `marked` library if it exists (full‑featured parser)
 *   • Falls back to a lightweight, safe parser that supports:
 *        – Headings (H1–H6)
 *        – Bold, italics, strikethrough
 *        – Unordered & ordered lists
 *        – Links, images, blockquotes, code blocks
 *   • Exposes a global `renderMarkdown(markdown)` function for
 *        programmatic use
 *   • Handles missing elements gracefully
 *   • Works on page load (DOMContentLoaded) and after dynamic DOM changes
 *
 * Usage:
 *   <textarea id="markdown-input"></textarea>
 *   <div id="markdown-output"></div>
 *
 *   // Manual rendering
 *   renderMarkdown('# Hello\n\nSome *markdown*');
 */
(function () {
  /* ---------- Utility helpers ---------- */
  const escapeHtml = (str) =>
    str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');

  /* ---------- Lightweight parser ---------- */
  const lightParse = (text) => {
    const lines = text.split('\n');
    const html = [];
    let inList = false;
    let listType = null; // 'ul' or 'ol'

    const flushList = () => {
      if (inList) {
        html.push(`</${listType}>`);
        inList = false;
        listType = null;
      }
    };

    for (let raw of lines) {
      let line = raw.trimEnd(); // preserve leading spaces for code blocks

      // Code block (fenced)
      if (/^