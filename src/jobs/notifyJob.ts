import { Worker, Job } from 'bullmq';
import nodemailer from 'nodemailer';
import { notifyQueue, StatusChangePayload } from '../queue/notifyQueue';

function formatSlackMessage(p: StatusChangePayload): string {
  return `:arrow_right: Request *${p.requestId}* status changed\n` +
         `• Old: \`${p.oldStatus}\`\n` +
         `• New: \`${p.newStatus}\`\n` +
         `• View: ${p.publicUrl}`;
}

function formatEmailDigest(p: StatusChangePayload): { subject: string; html: string } {
  const subject = `[Axentx] Request ${p.requestId} status changed: ${p.oldStatus} → ${p.newStatus}`;
  const html = `
    <p>Request <strong>${p.requestId}</strong> status changed.</p>
    <ul>
      <li>Old: <code>${p.oldStatus}</code></li>
      <li>New: <code>${p.newStatus}</code></li>
    </ul>
    <p><a href="${p.publicUrl}">View request</a></p>
    <p style="color:#666;font-size:12px">Automated notification from Axentx.</p>
  `;
  return { subject, html };
}

async function postToSlack(message: string): Promise<void> {
  const webhook = process.env.SLACK_WEBHOOK_URL;
  if (!webhook) {
    console.warn('SLACK_WEBHOOK_URL not configured — skipping Slack notification');
    return;
  }

  const res = await fetch(webhook, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: message }),
  });

  if (!res.ok) {
    const txt = await res.text().catch(() => '');
    throw new Error(`Slack webhook failed: ${res.status} ${res.statusText} ${txt}`);
  }
}

async function sendEmailDigest(payload: StatusChangePayload): Promise<void> {
  const subscribers = process.env.NOTIFY_EMAIL_SUBSCRIBERS;
  if (!subscribers?.trim()) {
    console.warn('NOTIFY_EMAIL_SUBSCRIBERS not configured — skipping email notification');
    return;
  }

  const { subject, html } = formatEmailDigest(payload);
  const smtpHost = process.env.SMTP_HOST;
  const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);
  const smtpUser = process.env.SMTP_USER;
  const smtpPass = process.env.SMTP_PASS;
  const from = process.env.SMTP_FROM || 'notifications@axentx.io';

  if (!smtpHost) {
    console.warn('SMTP_HOST not configured — skipping email send. Would send to:', subscribers);
    console.warn('Subject:', subject);
    return;
  }

  const transporter = nodemailer.createTransport({
    host: smtpHost,
    port: smtpPort,
    secure: smtpPort === 465,
    auth: smtpUser && smtpPass ? { user: smtpUser, pass: smtpPass } : undefined,
  });

  await transporter.sendMail({
    from,
    to: subscribers,
    subject,
    html,
  });
}

// Worker: email is primary (throw on failure), Slack is best-effort
const worker = new Worker<StatusChangePayload>(
  'status-notify',
  async (job: Job<StatusChangePayload>) => {
    const payload = job.data;

    // Slack is non-critical
    await postToSlack(formatSlackMessage(payload)).catch((err) => {
      console.error('Slack notification failed:', err.message);
    });

    // Email is critical — failure throws and triggers retry
    await sendEmailDigest(payload);
  },
  {
    connection: notifyQueue.client.options.connection,
    autorun: true,
  }
);

worker.on('failed', (job, err) => {
  console.error(`Job ${job?.id} failed:`, err.message);
});

// Graceful shutdown helper
export async function shutdownNotifyWorker(): Promise<void> {
  await worker.close();
}