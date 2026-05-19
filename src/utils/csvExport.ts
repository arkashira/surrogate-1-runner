/**
 * CSV Export Utility
 *
 * Generates a CSV string from an array of objects and triggers a download.
 * The API is intentionally generic – it can be used anywhere in the UI.
 *
 * Usage:
 *   import { exportToCsv } from '@/utils/csvExport';
 *
 *   const columns = [
 *     { header: 'Timestamp', key: 'timestamp' },
 *     { header: 'User', key: 'user' },
 *     { header: 'Field', key: 'field' },
 *     { header: 'Old Value', key: 'oldValue' },
 *     { header: 'New Value', key: 'newValue' },
 *   ];
 *
 *   exportToCsv(auditEntries, columns, 'audit-log.csv');
 */

export interface CsvColumn<T> {
  /** Header text that will appear as the first row */
  header: string;
  /** Property key on the data objects */
  key: keyof T;
}

/**
 * Escape a value for CSV output.
 *
 * - Wraps the value in double quotes if it contains a comma, double‑quote,
 *   newline, or carriage return.
 * - Double quotes inside the value are escaped by doubling them.
 */
export function escapeCsvValue(value: unknown): string {
  if (value === null || value === undefined) {
    return '';
  }
  const str = String(value);
  if (/[",\r\n]/.test(str)) {
    const escaped = str.replace(/"/g, '""');
    return `"${escaped}"`;
  }
  return str;
}

/**
 * Generate a CSV string from data and column definitions.
 *
 * @param data    Array of objects to be serialized.
 * @param columns Column definitions describing header order and object keys.
 * @returns CSV string (including header row, ending with a newline).
 */
export function generateCsv<T extends Record<string, unknown>>(
  data: T[],
  columns: CsvColumn<T>[],
): string {
  const headerRow = columns.map(col => escapeCsvValue(col.header)).join(',');
  const rows = data.map(item => {
    const row = columns.map(col => escapeCsvValue(item[col.key]));
    return row.join(',');
  });
  // Ensure final newline for compatibility with most spreadsheet apps
  return `${headerRow}\n${rows.join('\n')}\n`;
}

/**
 * Triggers a download of the supplied CSV string.
 *
 * @param csvString CSV content.
 * @param fileName  Desired filename (defaults to 'export.csv').
 */
export function downloadCsv(csvString: string, fileName = 'export.csv'): void {
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', fileName);
  // Append to body to make it work in Firefox
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Convenience wrapper that generates CSV from data/columns and immediately
 * starts a download.
 *
 * @param data     Data to export.
 * @param columns  Column definitions.
 * @param fileName Desired filename (optional).
 */
export function exportToCsv<T extends Record<string, unknown>>(
  data: T[],
  columns: CsvColumn<T>[],
  fileName?: string,
): void {
  const csv = generateCsv(data, columns);
  downloadCsv(csv, fileName);
}