
export type RequestPublicTimelineItem = {
  timestamp: string;
  event: string;
  actor?: string;
};

export type RequestPublicNextMilestone = {
  name: string;
  eta: string; // ISO 8601
};

export type RequestPublicResponse = {
  title: string;
  status: string;
  owner: string;
  sla: number | null; // SLA in hours (or null if not set)
  timeline: RequestPublicTimelineItem[];
  lastUpdated: string; // ISO 8601
  nextMilestone?: RequestPublicNextMilestone;
};

export type RequestRecord = {
  id: string;
  publicUrl: string;
  title: string;
  status: string;
  owner: string;
  slaHours: number | null;
  timeline: Array<{ ts: string | Date; event: string; actor?: string }>;
  lastUpdated: string | Date;
  milestones: Array<{
    name: string;
    due: string | Date | null;
    completed: boolean;
  }>;
  enabled: boolean;
};

/**
 * Serialize a request record for public consumption.
 * Omits internal fields and normalizes dates.
 */
export function serializeRequestPublic(record: RequestRecord): RequestPublicResponse {
  const lastUpdated = toISO(record.lastUpdated);

  const timeline = record.timeline
    .slice()
    .sort((a, b) => new Date(a.ts).getTime() - new Date(b.ts).getTime())
    .map((t) => ({
      timestamp: toISO(t.ts),
      event: t.event,
      actor: t.actor,
    }));

  // Next milestone: first incomplete milestone with a due date, sorted by due
  const upcoming = record.milestones
    .filter((m) => !m.completed && m.due != null)
    .sort((a, b) => new Date(a.due!).getTime() - new Date(b.due!).getTime())[0];

  const nextMilestone = upcoming
    ? {
        name: upcoming.name,
        eta: toISO(upcoming.due!),
      }
    : undefined;

  return {
    title: record.title,
    status: record.status,
    owner: record.owner,
    sla: record.slaHours,
    timeline,
    lastUpdated,
    nextMilestone,
  };
}

function toISO(value: string | Date | null | undefined): string {
  if (!value) return new Date().toISOString();
  if (typeof value === "string") return new Date(value).toISOString();
  return value.toISOString();
}