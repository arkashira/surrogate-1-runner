import { EventEmitter } from 'events';
import { setTimeout } from 'timers/promises';

/**
 * Memory monitor that tracks RSS memory usage and emits warnings
 * when memory exceeds thresholds.
 */
export class MemoryMonitor extends EventEmitter {
  private readonly thresholdMB: number;
  private readonly checkIntervalMs: number;
  private intervalId: NodeJS.Timeout | null = null;
  private isMonitoring = false;

  constructor(
    thresholdMB: number = 80,
    checkIntervalMs: number = 1000
  ) {
    super();
    this.thresholdMB = thresholdMB;
    this.checkIntervalMs = checkIntervalMs;
  }

  /**
   * Start monitoring memory usage
   */
  start(): void {
    if (this.isMonitoring) return;
    
    this.isMonitoring = true;
    this.intervalId = setInterval(() => {
      this.checkMemory();
    }, this.checkIntervalMs);
  }

  /**
   * Stop monitoring memory usage
   */
  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.isMonitoring = false;
  }

  /**
   * Check current memory usage and emit warning if threshold exceeded
   */
  private checkMemory(): void {
    const usage = process.memoryUsage();
    const rssMB = usage.rss / (1024 * 1024);

    if (rssMB > this.thresholdMB) {
      this.emit('memoryWarning', {
        rss: usage.rss,
        rssMB: Math.round(rssMB * 100) / 100,
        thresholdMB: this.thresholdMB
      });
    }
  }

  /**
   * Simulate memory usage for testing purposes
   */
  simulateMemoryUsage(sizeMB: number): void {
    // Create a large buffer to simulate memory usage
    const buffer = Buffer.alloc(sizeMB * 1024 * 1024, 0);
    // Keep reference to prevent garbage collection
    (global as any).__testBuffer = buffer;
  }

  /**
   * Clear simulated memory usage
   */
  clearSimulatedMemory(): void {
    delete (global as any).__testBuffer;
  }
}

/**
 * Utility function to create a memory-aware readable stream
 * @param readableStream - The underlying readable stream
 * @param memoryMonitor - Memory monitor instance
 * @returns A readable stream with back-pressure support
 */
export function createMemoryAwareReadable(
  readableStream: NodeJS.ReadableStream,
  memoryMonitor: MemoryMonitor
): NodeJS.ReadableStream {
  let isPaused = false;

  // Listen for memory warnings to control back-pressure
  memoryMonitor.on('memoryWarning', () => {
    if (!isPaused) {
      isPaused = true;
      readableStream.pause();
    }
  });

  // Resume when memory drops below threshold
  const resumeHandler = () => {
    if (isPaused) {
      isPaused = false;
      readableStream.resume();
    }
  };

  // Add a small delay to ensure memory drops before resuming
  memoryMonitor.on('memoryWarning', async () => {
    await setTimeout(100); // Small delay to allow memory cleanup
    resumeHandler();
  });

  return readableStream;
}