import fetch from 'node-fetch';

export interface SlackWebhookPayload {
  text?: string;
  blocks?: any[];
  attachments?: any[];
}

export async function sendSlackNotification(
  webhookUrl: string,
  payload: SlackWebhookPayload
): Promise<boolean> {
  if (!webhookUrl) {
    console.warn('No Slack webhook URL provided');
    return false;
  }

  try {
    const res = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const txt = await res.text().catch(() => '');
      console.error('Slack webhook failed', res.status, txt);
      return false;
    }

    return true;
  } catch (err) {
    console.error('Slack webhook error:', err);
    return false;
  }
}

export function formatSlackMessage(
  title: string,
  newStatus: string,
  publicUrl: string,
  slaState: 'on-tr
