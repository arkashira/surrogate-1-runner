+ import { buildRequestsQuery } from '../lib/query';

// Example using a lightweight router (adapt to your framework)
app.get('/requests', async (req, res) => {
  try {
+   const overdue = req.query.overdue === 'true';
+   const filters = { overdue };

+   const query = buildRequestsQuery(filters);
+   const requests = await db.query(query);

+   const results = requests.map((r: any) => {
+     const timeRemainingSec = Number(r.time_remaining_seconds);
+     const isOverdue = timeRemainingSec < 0;
+     const absHours = Math.floor(Math.abs(timeRemainingSec) / 3600);
+     const absMinutes = Math.floor((Math.abs(timeRemainingSec) % 3600) / 60);

+     let timeRemainingLabel = '';
+     if (isOverdue) {
+       timeRemainingLabel = `Overdue by ${absHours}h${absMinutes > 0 ? ` ${absMinutes}m` : ''}`;
+     } else {
+       timeRemainingLabel = `Due in ${absHours}h${absMinutes > 0 ? ` ${absMinutes}m` : ''}`;
+     }

+     return {
+       id: r.id,
+       created_at: r.created_at,
+       status: r.status,
+       sla_hours: r.sla_hours,
+       sla_deadline: r.sla_deadline,
+       time_remaining: timeRemainingLabel,
+       overdue: isOverdue,
+       _raw: {
+         time_remaining_seconds: timeRemainingSec
+       }
+     };
+   });

    res.json({
      requests: results,
+     count: results.length,
+     overdue_count: results.filter((r: any) => r.overdue).length
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});