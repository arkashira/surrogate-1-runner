/**
 * Data Export Utility
 *
 * Export arbitrary arrays of objects to CSV and trigger a download.
 * The API is intentionally small so it can be dropped into any UI.
 *
 * @module data-export
 */

export const DEFAULT_CONFIG = {
  /** default file name (without extension) */
  fileName: 'export',
  /** button label */
  buttonLabel: 'Export Data',
  /** CSV delimiter – comma, semicolon, tab, etc. */
  delimiter: ',',
  /** include header row (true) or not (false) */
  includeHeaders: true,
  /** add a timestamp to the file name (e.g. export-20240601T1530.csv) */
  timestamp: false,
  /** encoding – used only for the MIME type */
  encoding: 'utf-8',
};

/**
 * Escape a single CSV field.
 *
 * @private
 * @param {any} value
 * @returns {string}
 */
function escapeCsvValue(value) {
  if (value == null) return '';
  const str = String(value);
  if (/[",\n]/.test(str)) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

/**
 * Convert an array of objects to a CSV string.
 *
 * @param {Array<Object>} data
 * @param {Object} [options]
 * @param {string[]} [options.columns] – explicit column order; if omitted, keys of the first object are used
 * @param {string} [options.delimiter] – defaults to DEFAULT_CONFIG.delimiter
 * @param {boolean} [options.includeHeaders] – defaults to DEFAULT_CONFIG.includeHeaders
 * @returns {string}
 */
export function dataToCsv(
  data,
  { columns, delimiter = DEFAULT_CONFIG.delimiter, includeHeaders = DEFAULT_CONFIG.includeHeaders } = {}
) {
  if (!Array.isArray(data) || data.length === 0) return '';

  const cols = columns || Object.keys(data[0]);

  const rows = [];

  if (includeHeaders) {
    rows.push(cols.map(escapeCsvValue).join(delimiter));
  }

  data.forEach(row => {
    rows.push(cols.map(col => escapeCsvValue(row[col])).join(delimiter));
  });

  return rows.join('\n');
}

/**
 * Trigger a download of a text blob in the browser.
 *
 * @param {string} content
 * @param {string} fileName
 * @param {string} [encoding] – defaults to DEFAULT_CONFIG.encoding
 */
export function triggerDownload(content, fileName, encoding = DEFAULT_CONFIG.encoding) {
  const blob = new Blob([content], { type: `text/csv;charset=${encoding}` });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Attach an export button to a container element.
 *
 * @param {HTMLElement} containerEl
 * @param {Function} getDataFn – returns an array of objects
 * @param {Object} [options] – overrides DEFAULT_CONFIG
 */
export function attachExportButton(containerEl, getDataFn, options = {}) {
  if (!(containerEl instanceof HTMLElement)) {
    throw new Error('containerEl must be a valid HTMLElement');
  }
  if (typeof getDataFn !== 'function') {
    throw new Error('getDataFn must be a function returning an array of objects');
  }

  const cfg = { ...DEFAULT_CONFIG, ...options };

  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = cfg.buttonLabel;
  button.style.margin = '0.5rem';
  button.addEventListener('click', () => {
    try {
      const data = getDataFn();
      const csv = dataToCsv(data, { delimiter: cfg.delimiter });
      if (!csv) {
        // eslint-disable-next-line no-alert
        alert('No data available for export.');
        return;
      }

      const ts = cfg.timestamp
        ? `-${new Date().toISOString().replace(/[:.]/g, '-')}`
        : '';
      const fileName = `${cfg.fileName}${ts}.csv`;

      triggerDownload(csv, fileName, cfg.encoding);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('Data export failed:', err);
      // eslint-disable-next-line no-alert
      alert('Failed to export data. See console for details.');
    }
  });

  containerEl.appendChild(button);
}