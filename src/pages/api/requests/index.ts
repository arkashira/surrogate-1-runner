import type { NextApiRequest, NextApiResponse } from 'next';

// In-memory mock store — replace with DB in real system
let requests = [
  { id: '1', title: 'Access request', created_at: '2025-05-03T08:00:00.000Z', sla_hours: 24 },
  { id: '2', title: 'Password reset', created_at: '2025-05-02T08:00:00.000Z', sla_hours: 8 },
  { id: '3', title: 'Provision VM', created_at: '2025-05-03T10:00:00.000Z', sla_hours: 48 },
];

function computeSla(request: typeof requests[0]) {
  const created = new Date(request.created_at);
  const deadline = new Date(created.getTime() + request.sla_hours * 60 * 60 * 1000);
  const now = new Date();
  const diffMs = deadline.getTime() - now.getTime();
  const overdue = diffMs < 0;
  const absHours = Math.floor(Math.abs(diffMs) / (1000 * 60 * 60));
  const absMinutes = Math.floor((Math.abs(diffMs) % (1000 * 60 * 60)) / (1000 * 60));
  return {
    slaDeadline: deadline.toISOString(),
    isOverdue: overdue,
    timeRemaining: overdue
      ? `Overdue by ${absHours}h ${absMinutes}m`
      : `Due in ${absHours}h ${absMinutes}m`,
    timeRemainingMs: diffMs,
  };
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { overdue } = req.query;
  const enriched = requests.map((r) => ({ ...r, ...computeSla(r) }));

  if (overdue === 'true') {
    const overdueItems = enriched.filter((r) => r.isOverdue);
    return res.status(200).json({
      requests: overdueItems,
      count: overdueItems.length,
      total: enriched.length,
    });
  }

  res.status(200).json({ requests: enriched, count: enriched.length });
}