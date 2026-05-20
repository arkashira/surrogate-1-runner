const { v4: uuidv4 } = require('uuid');
const EventEmitter = require('events');
const nodemailer = require('nodemailer');
const mailTransport = require('../config/mail');

// -------------------------------------------------------------------
// 1️⃣  Event bus (shared by Socket.IO & SSE)
class OrderBus extends EventEmitter {}
const orderBus = new OrderBus();

// -------------------------------------------------------------------
// 2️⃣  In‑memory store (replace with DB later)
const orders = new Map(); // orderId → order object

// -------------------------------------------------------------------
// 3️⃣  Helper – send email to both parties
async function _notifyByEmail(order, subject, text) {
  const mailOptions = {
    from: '"Axentx Orders" <no-reply@axentx.com>',
    to: `${order.brandEmail}, ${order.manufacturerEmail}`,
    subject,
    text,
  };
  await mailTransport.sendMail(mailOptions);
}

// -------------------------------------------------------------------
// 4️⃣  Public API ----------------------------------------------------
/**
 * Place a new order.
 * @param {Object} payload { brandId, manufacturerId, brandEmail, manufacturerEmail, items }
 * @returns {Object} created order
 */
async function placeOrder(payload) {
  const id = uuidv4();
  const now = new Date();

  const order = {
    id,
    brandId: payload.brandId,
    manufacturerId: payload.manufacturerId,
    brandEmail: payload.brandEmail,
    manufacturerEmail: payload.manufacturerEmail,
    items: payload.items || [],
    status: 'PENDING',
    createdAt: now,
    updatedAt: now,
  };

  orders.set(id, order);

  // Notify immediately (status = PENDING)
  const subject = `Order ${id} placed`;
  const body = `Your order ${id} has been created and is currently PENDING.`;
  await _notifyByEmail(order, subject, body);

  // Emit real‑time event
  orderBus.emit('status-updated', { orderId: id, order });

  return order;
}

/**
 * Update order status.
 * @param {string} orderId
 * @param {string} newStatus e.g. IN_PRODUCTION, SHIPPED, COMPLETED
 * @returns {Object} updated order
 */
async function updateOrderStatus(orderId, newStatus) {
  const order = orders.get(orderId);
  if (!order) throw new Error('Order not found');

  order.status = newStatus;
  order.updatedAt = new Date();

  // Email notification
  const subject = `Order ${orderId} status: ${newStatus}`;
  const body = `The order ${orderId} status changed to "${newStatus}".`;
  await _notifyByEmail(order, subject, body);

  // Real‑time broadcast
  orderBus.emit('status-updated', { orderId, order });

  return order;
}

/**
 * Retrieve an order (read‑only copy).
 */
function getOrder(orderId) {
  const order = orders.get(orderId);
  return order ? { ...order } : null;
}

/**
 * Expose the bus so the HTTP layer can subscribe.
 */
function getBus() {
  return orderBus;
}

module.exports = {
  placeOrder,
  updateOrderStatus,
  getOrder,
  getBus,
};