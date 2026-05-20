/**
 * Convert an array of objects to a CSV string.
 * Keys of the first object define the column order.
 */
export function toCSV<T extends Record<string, unknown>>(rows: T[]): string {
  if (!rows.length) return '';

  const header = Object.keys(rows[0]);
  const escape = (value: unknown) => {
    const str = String(value ?? '');
    // Escape double quotes and wrap fields that contain commas, quotes or newlines
    return /[",\n]/.test(str) ? `"${str.replace(/"/g, '""')}"` : str;
  };

  const lines = [
    header.join(','), // header row
    ...rows.map(row => header.map(col => escape(row[col])).join(',')),
  ];

  return lines.join('\n');
}