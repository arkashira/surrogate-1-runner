+ import { sql } from './db'; // or your DB client

export interface RequestFilters {
  overdue?: boolean;
  // ... other filters
}

export function buildRequestsQuery(filters: RequestFilters) {
  let query = sql`
    SELECT
      id,
      created_at,
      status,
      sla_hours,
+     created_at + (sla_hours || ' hours')::interval AS sla_deadline,
+     EXTRACT(EPOCH FROM (created_at + (sla_hours || ' hours')::interval - NOW())) AS time_remaining_seconds
    FROM requests
    WHERE 1=1
  `;

  if (filters.overdue === true) {
    query += sql`
      AND (created_at + (sla_hours || ' hours')::interval) < NOW()
    `;
  }

  // Add other filters here (status, assignee, etc.)

  query += sql` ORDER BY sla_deadline ASC`;
  return query;
}