import { sendMail } from './mailer';

/**
 * Sends a password‑reset e‑mail.
 *
 * @param userEmail  Recipient e‑mail address
 * @param resetToken Token that will be embedded in the reset link
 *
 * @throws If required env vars are missing or if the e‑mail fails to send
 */
export async function sendPasswordResetEmail(
  userEmail: string,
  resetToken: string
): Promise<void> {
  // Basic argument validation
  if (!userEmail) throw new Error('Missing userEmail');
  if (!resetToken) throw new Error('Missing resetToken');

  // ------------------------------------------------------------------
  // Build the reset link
  // ------------------------------------------------------------------
  const { PASSWORD_RESET_URL, FRONTEND_URL } = process.env;

  let resetLink: string;
  if (PASSWORD_RESET_URL) {
    resetLink = `${PASSWORD_RESET_URL}?token=${encodeURIComponent(resetToken)}`;
  } else if (FRONTEND_URL) {
    const base = FRONTEND_URL.replace(/\/$/, ''); // strip trailing slash
    resetLink = `${base}/reset-password?token=${encodeURIComponent(resetToken)}`;
  } else {
    throw new Error(
      'Neither PASSWORD_RESET_URL nor FRONTEND_URL is set in the environment.'
    );
  }

  // ------------------------------------------------------------------
  // Email body
  // ------------------------------------------------------------------
  const subject = 'Reset Your Password';
  const text = `You requested a password reset. Click the link below to set a new password:\n\n${resetLink}\n\nIf you did not request this, please ignore this e‑mail.`;
  const html = `
    <p>Hello,</p>
    <p>You requested a password reset. Click the link below to set a new password:</p>
    <p><a href="${resetLink}">Reset Password</a></p>
    <p>If you did not request this, you can safely ignore this e‑mail.</p>
    <p>Thanks,<br/>The AxentX Team</p>
  `;

  // ------------------------------------------------------------------
  // Send the e‑mail
  // ------------------------------------------------------------------
  await sendMail(userEmail, subject, html, text);
}