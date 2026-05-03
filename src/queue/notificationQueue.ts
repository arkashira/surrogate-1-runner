// routes/requests.ts
describe('PATCH /requests/:id/status', () => {
  test('enqueues notification job on status change with correct payload and dedupe id', async () => {
    const req = { id: 'req-1', title: 'Demo', status: 'open', publicUrl: 'https://app/req-1' };
    const actor = { id: 'u-1', name: 'Alice' };
    const queue = { add: vi.fn() };
    const repo = { findById: vi.fn().mockResolvedValue(req), updateStatus: vi.fn().mockResolvedValue({ ...req, status: 'in_progress' }) };

    await handler({ repo, queue, actor, requestId: 'req-1', body: { status: 'in_progress' } });

    expect(queue.add).toHaveBeenCalledWith(
      'notifications',
      { requestId: 'req-1', title: 'Demo', newStatus: 'in_progress', publicUrl: 'https://app/req-1', actor },
      { deduplicationId: 'notif:req-1', delay: 0, attempts: 3, backoff: { type: 'exponential', delay: 2000 }, removeOnComplete: true, removeOnFail: true }
    );
  });

  test('does not enqueue when status unchanged', async () => {
    const req = { id: 'req-1', status: 'open' };
    const queue = { add: vi.fn() };
    const repo = { findById: vi.fn().mockResolvedValue(req), updateStatus: vi.fn().mockResolvedValue(req) };

    const res = await handler({ repo, queue, actor: {}, requestId: 'req-1', body: { status: 'open' } });

    expect(queue.add).not.toHaveBeenCalled();
    expect(res.status).toBe(200);
  });

  test('returns 404 when request not found', async () => {
    const repo = { findById: vi.fn().mockResolvedValue(null) };
    const res = await handler({ repo, queue: { add: vi.fn() }, actor: {}, requestId: 'req-1', body: { status: 'in_progress' } });
    expect(res.status).toBe(404);
  });
});

// queue/notificationQueue.ts
describe('NotificationWorker', () => {
  test('posts Slack message when SLACK_WEBHOOK_URL is set', async () => {
    process.env.SLACK_WEBHOOK_URL = 'https://hooks.slack.com/xxx';
    const fetch = vi.spyOn(global, 'fetch').mockResolvedValue({ ok: true } as any);
    const job = { data: { requestId: 'req-1', title: 'Demo', newStatus: 'in_progress', publicUrl: 'https://app/req-1', actor: { name: 'Alice' } } };

    await worker.process(job);
    expect(fetch).toHaveBeenCalledWith(process.env.SLACK_WEBHOOK_URL, expect.objectContaining({ method: 'POST' }));
    const payload = JSON.parse((fetch as any).mock.calls[0][1].body);
    expect(payload.text).toContain('Demo');
    expect(payload.text).toContain('in_progress');
  });

  test('sends email when EMAIL_SMTP_URL and NOTIFICATION_EMAIL_RECIPIENTS are set', async => {
    process.env.EMAIL_SMTP_URL = 'smtps://user:pass@host';
    process.env.NOTIFICATION_EMAIL_RECIPIENTS = 'team@example.com';
    const nodemailer = { createTransport: vi.fn().mockReturnValue({ sendMail: vi.fn().mockResolvedValue(true) }) };
    const job = { data: { requestId: 'req-1', title: 'Demo', newStatus: 'in_progress', publicUrl: 'https://app/req-1', actor: { name: 'Alice' } } };

    await worker.process(job);
    expect(nodemailer.createTransport().sendMail).toHaveBeenCalledWith(expect.objectContaining({
      to: 'team@example.com',
      subject: expect.stringContaining('Demo'),
      text: expect.stringContaining('in_progress')
    }));
  });
});