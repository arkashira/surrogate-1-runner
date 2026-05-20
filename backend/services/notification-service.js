/* --------------------------------------------------------------
   Central notification hub
   - Email via nodemailer (SMTP)
   - In‑app push via EventEmitter (SSE or Socket.IO)
   - Exported `notifyOrderUpdate` for order‑service consumption
   -------------------------------------------------------------- */

const nodemailer = require('nodemailer');
const { EventEmitter } = require('events');
const logger = console; // replace with your logger in production

// ------------------------------------------------------------------
// 1️⃣  Email transport
// ------------------------------------------------------------------
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST || 'smtp.example.com',
  port: parseInt(process.env.SMTP_PORT, 10) || 587,
  secure: false, // true for 465, false for other ports
  auth: {
    user: process.env.SMTP_USER || 'user@example.com',
    pass: process.env.SMTP_PASS || 'password',
  },
});

/**
 * Send a single email.
 * @param {Object} opts
 * @param {string} opts.to        Recipient address
 * @param {string} opts.subject   Subject line
 * @param {string} opts.html      HTML body
 */
async function sendEmail({ to, subject, html }) {
  const mailOptions = {
    from: process.env.SMTP_FROM || '"Axentx" <no-reply@axentx.com>',
    to,
    subject,
    html,
  };
  await transporter.sendMail(mailOptions);
}

// ------------------------------------------------------------------
// 2️⃣  In‑app notification emitter
// ------------------------------------------------------------------
/**
 * The emitter is deliberately simple – it can be swapped for a real
 * pub/sub (Redis, NATS, Kafka) without changing the public API.
 */
const notificationEmitter = new EventEmitter();

/**
 * Emit a notification for a specific user.
 * @param {string} userId   The logical user identifier
 * @param {Object} payload  Arbitrary payload that the UI will render
 */
function emitInApp(userId, payload) {
  // Namespaced event makes it easy for SSE/WS layers to filter per user
  notificationEmitter.emit(`notification:${userId}`, payload);
}

// ------------------------------------------------------------------
// 3️⃣  Public helper – order status broadcast
// ------------------------------------------------------------------
/**
 * Notify brand & manufacturer that an order changed status.
 *
 * @param {Object} order
 *   { id, brand: { id, userId, email, name },
 *     manufacturer: { id, userId, email, name } }
 * @param {string} newStatus   Human‑readable status (e.g. "Shipped")
 */
async function notifyOrderUpdate(order, newStatus) {
  const { id, brand, manufacturer } = order;

  // ----------------------------------------------------------------
  // 3a️⃣ Build email content (same template for both parties)
  // ----------------------------------------------------------------
  const subject = `Order #${id} status updated to ${newStatus}`;
  const html = `
    <p>Hi ${brand.name},</p>
    <p>Your order <strong>#${id}</strong> is now <em>${newStatus}</em>.</p>
    <p>Best regards,<br/>${manufacturer.name}</p>
  `;

  // ----------------------------------------------------------------
  // 3b️⃣ Send e‑mail (fire‑and‑forget each, but await to surface errors)
  // ----------------------------------------------------------------
  try {
    await Promise.all([
      sendEmail({ to: brand.email, subject, html }),
      sendEmail({ to: manufacturer.email, subject, html }),
    ]);
  } catch (err) {
    logger.error('📧 Email notification failed', { err, orderId: id });
    // Continue – we still want the in‑app push
  }

  // ----------------------------------------------------------------
  // 3c️⃣ Emit in‑app payload (same for both users)
  // ----------------------------------------------------------------
  const payload = {
    orderId: id,
    status: newStatus,
    title: `Order ${id} status update`,
    message: `Your order is now ${newStatus}.`,
    timestamp: new Date().toISOString(),
  };

  try {
    emitInApp(brand.userId, payload);
    emitInApp(manufacturer.userId, payload);
  } catch (err) {
    logger.error('🔔 In‑app notification emit failed', { err, orderId: id });
  }
}

// ------------------------------------------------------------------
// 4️⃣  Exported API
// ------------------------------------------------------------------
module.exports = {
  // Business‑logic entry point
  notifyOrderUpdate,

  // Low‑level primitives (useful for tests or custom flows)
  sendEmail,
  emitInApp,
  notificationEmitter,
};