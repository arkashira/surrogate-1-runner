/**
 * Task Scheduler Service
 *
 * This module provides a simple cron‑based scheduling system for data
 * generation tasks. It supports three scheduling options:
 *   - "now"      : run immediately
 *   - "in1h"     : run one hour from the time of scheduling
 *   - "daily"    : run once a day at 00:00 UTC
 *
 * Scheduled tasks are persisted in `tasks.json` so that the service
 * can recover after a restart.  When a task is scheduled, a confirmation
 * email is sent to the creator.
 *
 * Dependencies:
 *   - node-cron
 *   - nodemailer
 *
 * Usage:
 *   const { scheduleTask, startScheduler } = require('./taskScheduler');
 *   startScheduler(); // call once on service start
 *   scheduleTask(instanceId, 'in1h', 'user@example.com');
 */

const fs = require('fs');
const path = require('path');
const cron = require('node-cron');
const nodemailer = require('nodemailer');

// Path to the persistent task store
const TASKS_FILE = path.join(__dirname, '..', 'tasks.json');

// In‑memory task registry
const tasks = new Map();

/**
 * Load persisted tasks from disk and schedule them.
 */
function loadPersistedTasks() {
  if (!fs.existsSync(TASKS_FILE)) {
    return;
  }
  const data = JSON.parse(fs.readFileSync(TASKS_FILE, 'utf8'));
  data.forEach((task) => {
    scheduleCronJob(task);
  });
}

/**
 * Persist current task registry to disk.
 */
function persistTasks() {
  const data = Array.from(tasks.values());
  fs.writeFileSync(TASKS_FILE, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Create a nodemailer transporter.
 * In production, replace the test account with real SMTP credentials.
 */
const transporter = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  secure: false,
  auth: {
    user: 'noreply@example.com',
    pass: 'password',
  },
});

/**
 * Send a confirmation email for a scheduled task.
 *
 * @param {string} email - Recipient email address
 * @param {object} task  - Task details
 */
async function sendConfirmationEmail(email, task) {
  const mailOptions = {
    from: '"Axentx Scheduler" <noreply@example.com>',
    to: email,
    subject: `Task Scheduled: ${task.instanceId}`,
    text: `Your data generation task for instance ${task.instanceId} has been scheduled.\n\n` +
          `Schedule: ${task.scheduleOption}\n` +
          `Next run: ${new Date(task.nextRun).toISOString()}\n\n` +
          `Thank you for using Axentx!`,
  };
  try {
    await transporter.sendMail(mailOptions);
  } catch (err) {
    console.error('Failed to send confirmation email:', err);
  }
}

/**
 * Execute the data generation logic for a given instance.
 * This is a placeholder; replace with real implementation.
 *
 * @param {string} instanceId
 */
function runDataGeneration(instanceId) {
  console.log(`[${new Date().toISOString()}] Running data generation for instance ${instanceId}`);
  // TODO: Insert actual data generation logic here.
}

/**
 * Schedule a cron job based on the task definition.
 *
 * @param {object} task
 */
function scheduleCronJob(task) {
  // Cancel any existing job for this task
  if (task.job) {
    task.job.stop();
  }

  // Determine cron expression
  let cronExpression;
  if (task.scheduleOption === 'daily') {
    // Run at midnight UTC
    cronExpression = '0 0 * * *';
  } else if (task.scheduleOption === 'in1h') {
    // One‑hour delay: compute exact timestamp and use a one‑time job
    const runAt = new Date(task.nextRun);
    const delayMs = runAt - Date.now();
    if (delayMs <= 0) {
      // Time already passed; run immediately
      runDataGeneration(task.instanceId);
      // Update nextRun to next day
      task.nextRun = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
      persistTasks();
      return;
    }
    // Use setTimeout for one‑time execution
    task.job = setTimeout(() => {
      runDataGeneration(task.instanceId);
      // Reschedule for next day
      task.nextRun = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
      persistTasks();
      // After one‑time run, schedule daily cron
      scheduleCronJob(task);
    }, delayMs);
    tasks.set(task.id, task);
    persistTasks();
    return;
  } else {
    // Default to immediate execution
    cronExpression = '* * * * *'; // every minute, but we will run once
  }

  // Schedule recurring job
  task.job = cron.schedule(cronExpression, () => {
    runDataGeneration(task.instanceId);
  });
  tasks.set(task.id, task);
  persistTasks();
}

/**
 * Public API
 */

/**
 * Schedule a new task.
 *
 * @param {string} instanceId
 * @param {string} scheduleOption - 'now', 'in1h', 'daily'
 * @param {string} email - Recipient email address
 */
async function scheduleTask(instanceId, scheduleOption, email) {
  const id = `${instanceId}-${Date.now()}`;
  let nextRun;
  if (scheduleOption === 'now') {
    nextRun = new Date().toISOString();
    runDataGeneration(instanceId);
  } else if (scheduleOption === 'in1h') {
    nextRun = new Date(Date.now() + 60 * 60 * 1000).toISOString();
  } else if (scheduleOption === 'daily') {
    // Set to next midnight UTC
    const now = new Date();
    const nextMidnight = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1));
    nextRun = nextMidnight.toISOString();
  } else {
    throw new Error(`Unsupported schedule option: ${scheduleOption}`);
  }

  const task = {
    id,
    instanceId,
    scheduleOption,
    email,
    nextRun,
    job: null,
  };

  scheduleCronJob(task);
  await sendConfirmationEmail(email, task);
  return task;
}

/**
 * Start the scheduler by loading persisted tasks.
 */
function startScheduler() {
  loadPersistedTasks();
}

module.exports = {
  scheduleTask,
  startScheduler,
};