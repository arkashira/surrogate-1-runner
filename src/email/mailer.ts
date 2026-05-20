import nodemailer, { Transporter } from 'nodemailer';
import { config } from 'dotenv';

config(); // Loads .env into process.env

/**
 * Lazily creates a Nodemailer transporter the first time it is needed.
 * Subsequent calls reuse the same instance – this keeps the overhead low.
 */
let transporter: Transporter | null = null;

export function getTransporter(): Transporter {
  if (transporter) return transporter;

  const {
    SMTP_HOST,
    SMTP_PORT,
    SMTP_SECURE,
    SMTP_USER,
    SMTP_PASS,
  } = process.env;

  if (!SMTP_HOST || !SMTP_PORT || !SMTP_USER || !SMTP_PASS) {
    throw new Error(
      'Missing required SMTP configuration (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS).'
    );
  }

  transporter = nodemailer.createTransport({
    host: SMTP_HOST,
    port: Number(SMTP_PORT),
    secure: SMTP_SECURE === 'true', // 465 = true, 587 = false
    auth: {
      user: SMTP_USER,
      pass: SMTP_PASS,
    },
  });

  return transporter;
}

/**
 * Sends an e‑mail using the shared transporter.
 *
 * @param to      Recipient address
 * @param subject Subject line
 * @param html    HTML body
 * @param text    Plain‑text body (optional)
 */
export async function sendMail(
  to: string,
  subject: string,
  html: string,
  text?: string
): Promise<void> {
  const transporter = getTransporter();

  await transporter.sendMail({
    from: process.env.EMAIL_FROM ?? '"Support" <support@example.com>',
    to,
    subject,
    text,
    html,
  });
}