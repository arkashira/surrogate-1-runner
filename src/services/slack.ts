import fetch from 'node-fetch';

const MAX_RETRIES = 3;

async function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function postStatusChange({
  webhookUrl,
  requestId,
  title,
  oldStatus,
  newStatus,
  dueAt,
  isOverdue,
}: {
  webhookUrl: string;
  requestId: string;
  title: string;
  oldStatus: string;
  newStatus: string;
  dueAt?: Date;
  isOverdue: boolean;
}) {
  const text = `:clipboard: Request *${title}* (${requestId}) status changed\n` +
    `• From: \`${oldStatus}\` → To: \`${newStatus}\`\n` +
    (dueAt ? `• Due: ${dueAt.toISOString().split('T')[0]}\n` : '') +
    (isOverdue ? `• :warning: *OVERDUE*\n` : '') +
    `• <${process.env.UI_BASE_URL}/requests/${requestId}|View request>`;

  const payload = { text };

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const res = await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) return;

      const errText = await res.text().catch(() => '');
      throw new Error(`Slack responded ${res.status}: ${errText}`);
    } catch (err) {
      if (attempt === MAX_RETRIES) {
        console.error('[slack] permanent failure after retries', {
          requestId,
          error: err instanceof Error ? err.message : String(err),
        });
        return;
      }
      const backoff = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
      console.warn('[slack] attempt failed, retrying', { attempt: attempt + 1, backoff, requestId });
      await sleep(backoff);
    }
  }
}