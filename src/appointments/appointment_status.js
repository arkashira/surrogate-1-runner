/**
 * Real-time Appointment Status Management System
 *
 * Provides comprehensive appointment status tracking with:
 * - Real-time status updates
 * - Event-driven architecture
 * - Status history tracking
 * - Multi-channel notifications
 * - Calendar integration
 *
 * Designed for production use with proper error handling and extensibility
 */

const EventEmitter = require('events');
const { v4: uuidv4 } = require('uuid');

/**
 * Appointment status enumeration
 * @readonly
 * @enum {string}
 */
const AppointmentStatus = {
  SCHEDULED: 'scheduled',
  CONFIRMED: 'confirmed',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
  NO_SHOW: 'no_show',
  RESCHEDULED: 'rescheduled',
  PENDING: 'pending'
};

/**
 * Appointment Status Manager
 * Core class for managing appointment statuses with history tracking
 */
class AppointmentStatusManager extends EventEmitter {
  constructor(options = {}) {
    super();
    this.appointments = new Map();
    this.statusHistory = new Map();
    this.maxHistorySize = options.maxHistorySize || 50;
    this.setMaxListeners(options.maxListeners || 100);
  }

  /**
   * Create a new appointment
   * @param {Object} details - Appointment details
   * @param {string} details.customerId
   * @param {Date} details.startTime
   * @param {Date} details.endTime
   * @param {string} details.location
   * @returns {string} appointmentId
   */
  createAppointment(details) {
    const id = uuidv4();
    const appointment = {
      id,
      customerId: details.customerId,
      startTime: details.startTime,
      endTime: details.endTime,
      location: details.location,
      status: AppointmentStatus.SCHEDULED,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    this.appointments.set(id, appointment);
    this._addToHistory(id, {
      status: AppointmentStatus.SCHEDULED,
      timestamp: appointment.createdAt
    });

    return id;
  }

  /**
   * Update appointment status
   * @param {string} appointmentId
   * @param {string} newStatus
   * @param {Object} metadata - Additional metadata
   * @returns {Object} Updated appointment
   * @throws {Error} If appointment not found or invalid status
   */
  updateStatus(appointmentId, newStatus, metadata = {}) {
    if (!this.appointments.has(appointmentId)) {
      throw new Error(`Appointment ${appointmentId} not found`);
    }

    if (!Object.values(AppointmentStatus).includes(newStatus)) {
      throw new Error(`Invalid status: ${newStatus}`);
    }

    const appointment = this.appointments.get(appointmentId);
    const previousStatus = appointment.status;
    const now = new Date().toISOString();

    appointment.status = newStatus;
    appointment.updatedAt = now;
    Object.assign(appointment, metadata);

    this._addToHistory(appointmentId, {
      status: newStatus,
      previousStatus,
      timestamp: now,
      metadata
    });

    // Emit events
    this.emit('statusUpdated', {
      appointmentId,
      previousStatus,
      newStatus,
      timestamp: now,
      metadata
    });
    this.emit(`status:${newStatus}`, {
      appointmentId,
      timestamp: now
    });

    // Notify channels
    this._notifyChannels(appointment);

    return appointment;
  }

  /**
   * Get appointment status history
   * @param {string} appointmentId
   * @returns {Array} Status history entries
   */
  getStatusHistory(appointmentId) {
    return this.statusHistory.get(appointmentId) || [];
  }

  /**
   * Subscribe to status updates
   * @param {string} eventName - Event to subscribe to (e.g., 'statusUpdated' or 'status:confirmed')
   * @param {Function} callback
   */
  onStatusUpdate(eventName, callback) {
    this.on(eventName, callback);
  }

  /**
   * Integrate with external calendar system
   * @param {string} appointmentId
   * @returns {boolean} Integration success status
   */
  async integrateWithCalendar(appointmentId) {
    if (!this.appointments.has(appointmentId)) {
      return false;
    }

    const appointment = this.appointments.get(appointmentId);

    // In production, replace with actual calendar API integration
    console.log(`[Calendar Integration] Processing appointment ${appointmentId} for calendar sync`);
    console.log(`Event details: ${JSON.stringify({
      start: appointment.startTime,
      end: appointment.endTime,
      location: appointment.location
    })}`);

    // Simulate API call
    return new Promise(resolve => {
      setTimeout(() => {
        console.log(`[Calendar Integration] Successfully synced appointment ${appointmentId}`);
        resolve(true);
      }, 1000);
    });
  }

  /**
   * Internal method to add status to history
   * @private
   */
  _addToHistory(appointmentId, entry) {
    if (!this.statusHistory.has(appointmentId)) {
      this.statusHistory.set(appointmentId, []);
    }

    const history = this.statusHistory.get(appointmentId);
    history.push(entry);

    // Enforce max history size
    if (history.length > this.maxHistorySize) {
      history.shift();
    }
  }

  /**
   * Internal method to notify channels
   * @private
   */
  _notifyChannels(appointment) {
    // In production, replace with actual notification services
    console.log(`[Notification] Sending status update for appointment ${appointment.id}`);
    console.log(`[SMS] Appointment ${appointment.id} status changed to ${appointment.status}`);
    console.log(`[Email] Appointment ${appointment.id} status changed to ${appointment.status}`);
    console.log(`[Push] Appointment ${appointment.id} status changed to ${appointment.status}`);
  }
}

module.exports = {
  AppointmentStatusManager,
  AppointmentStatus
};