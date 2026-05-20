/**
 * A lightweight, cron‑style scheduler.
 * - Per‑task intervals (default 1 min)
 * - Immediate execution flag
 * - Automatic next‑run calculation
 * - Graceful error handling
 * - Status API for monitoring
 */

class Scheduler {
  constructor({ defaultInterval = 60_000 } = {}) {
    this.defaultInterval = defaultInterval;
    this.tasks = new Map();          // name → task meta
    this.running = false;
    this.timer = null;
  }

  /** Register a new task */
  addTask(name, fn, { interval, immediate = false } = {}) {
    if (this.tasks.has(name)) {
      throw new Error(`Task "${name}" already exists`);
    }

    const meta = {
      fn,
      interval: interval ?? this.defaultInterval,
      immediate,
      lastRun: null,
      nextRun: null,
    };

    this.tasks.set(name, meta);

    if (immediate) this.runTask(name);

    return this;
  }

  /** Remove a task */
  removeTask(name) {
    this.tasks.delete(name);
    return this;
  }

  /** Execute a single task */
  async runTask(name) {
    const task = this.tasks.get(name);
    if (!task) throw new Error(`Task "${name}" not found`);

    const start = Date.now();
    try {
      await task.fn();
      task.lastRun = start;
      task.nextRun = Date.now() + task.interval;
      console.log(`[Scheduler] "${name}" finished @ ${new Date().toISOString()}`);
    } catch (err) {
      console.error(`[Scheduler] "${name}" error:`, err);
      task.lastRun = start;
      task.nextRun = Date.now() + task.interval;
    }
  }

  /** Scheduler loop – called every `defaultInterval` */
  tick() {
    const now = Date.now();
    for (const [name, task] of this.tasks) {
      if (!task.nextRun || now >= task.nextRun) {
        this.runTask(name).catch(err => console.error(`[Scheduler] ${name} failed`, err));
      }
    }
  }

  /** Start the scheduler */
  start() {
    if (this.running) return this;
    this.running = true;
    console.log('[Scheduler] started');
    this.timer = setInterval(() => this.tick(), this.defaultInterval);
    return this;
  }

  /** Stop the scheduler */
  stop() {
    if (!this.running) return this;
    this.running = false;
    clearInterval(this.timer);
    this.timer = null;
    console.log('[Scheduler] stopped');
    return this;
  }

  /** Human‑readable status */
  getStatus() {
    return {
      running: this.running,
      tasks: Array.from(this.tasks.entries()).map(([name, t]) => ({
        name,
        interval: t.interval,
        lastRun: t.lastRun ? new Date(t.lastRun).toISOString() : null,
        nextRun: t.nextRun ? new Date(t.nextRun).toISOString() : null,
      })),
    };
  }
}

module.exports = { Scheduler };