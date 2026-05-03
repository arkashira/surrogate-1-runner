
import { pgTable, serial, text, timestamp, varchar } from 'drizzle-orm/pg-core';

export const requestStatusHistory = pgTable('request_status_history', {
  id: serial('id').primaryKey(),
  requestId: varchar('request_id', { length: 64 }).notNull(),
  fromStatus: varchar('from_status', { length: 32 }), // nullable for initial
  toStatus: varchar('to_status', { length: 32 }).notNull(),
  actor: varchar('actor', { length: 128 }).notNull(),
  comment: text('comment').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

// Optional: index for fast history lookups
// (run in migration)