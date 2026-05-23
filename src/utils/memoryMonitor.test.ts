import { describe, it, beforeEach, afterEach, expect, vi } from 'vitest';
import { MemoryMonitor, createMemoryAwareReadable } from './memoryMonitor';
import { Readable } from 'stream';

describe('MemoryMonitor', () => {
  let monitor: MemoryMonitor;

  beforeEach(() => {
    monitor = new MemoryMonitor(80, 100);
    vi.useFakeTimers();
  });

  afterEach(() => {
    monitor.stop();
    vi.useRealTimers();
  });

  it('should emit memoryWarning when RSS exceeds threshold', () => {
    const spy = vi.fn();
    monitor.on('memoryWarning', spy);
    
    // Simulate high memory usage
    monitor.simulateMemoryUsage(100);
    
    // Advance time to trigger check
    vi.advanceTimersByTime(100);
    
    expect(spy).toHaveBeenCalled();
    
    // Clean up
    monitor.clearSimulatedMemory();
  });

  it('should not emit memoryWarning when RSS is below threshold', () => {
    const spy = vi.fn();
    monitor.on('memoryWarning', spy);
    
    // Simulate low memory usage
    monitor.simulateMemoryUsage(50);
    
    // Advance time to trigger check
    vi.advanceTimersByTime(100);
    
    expect(spy).not.toHaveBeenCalled();
    
    // Clean up
    monitor.clearSimulatedMemory();
  });

  it('should start and stop monitoring correctly', () => {
    expect(monitor['isMonitoring']).toBe(false);
    
    monitor.start();
    expect(monitor['isMonitoring']).toBe(true);
    
    monitor.stop();
    expect(monitor['isMonitoring']).toBe(false);
  });
});

describe('createMemoryAwareReadable', () => {
  it('should handle back-pressure correctly', () => {
    const mockStream = new Readable({
      read() {}
    });
    
    const monitor = new MemoryMonitor(80, 100);
    
    // Mock pause and resume methods
    const pauseSpy = vi.spyOn(mockStream, 'pause');
    const resumeSpy = vi.spyOn(mockStream, 'resume');
    
    const memoryAwareStream = createMemoryAwareReadable(mockStream, monitor);
    
    // Simulate memory warning
    monitor.simulateMemoryUsage(100);
    
    // Trigger memory check
    vi.advanceTimersByTime(100);
    
    // Should have paused
    expect(pauseSpy).toHaveBeenCalled();
    
    // Clean up
    monitor.clearSimulatedMemory();
  });
});