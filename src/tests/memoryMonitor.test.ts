import { MemoryMonitor } from '../lib/MemoryMonitor';
import { Readable } from 'stream';

describe('MemoryMonitor', () => {
  let memoryMonitor: MemoryMonitor;
  let mockReadableStream: Readable;

  beforeEach(() => {
    memoryMonitor = new MemoryMonitor();
    mockReadableStream = new Readable({
      read() {
        // Simulate data being pushed into the stream
        this.push(Buffer.alloc(1024 * 1024)); // 1 MB chunks
      }
    });
  });

  it('should emit memoryWarning event when RSS exceeds 80 MB', async () => {
    const memoryWarningSpy = jest.spyOn(memoryMonitor, 'emit');
    memoryMonitor.monitor(mockReadableStream);

    // Simulate rapid data bursts
    for (let i = 0; i < 80; i++) {
      mockReadableStream.read();
    }

    expect(memoryWarningSpy).toHaveBeenCalledWith('memoryWarning');
  });

  it('should allow upstream to pause/resume the readable stream', async () => {
    memoryMonitor.monitor(mockReadableStream);
    memoryMonitor.emit('memoryWarning');

    expect(mockReadableStream.isPaused()).toBe(true);

    memoryMonitor.resumeStream();
    expect(mockReadableStream.isPaused()).toBe(false);
  });
});