package com.axentx.surrogate1;

/**
 * Immutable snapshot of system resources used for adaptive configuration.
 */
public final class SystemResources {
    private final long freeHeapBytes;
    private final long totalHeapBytes;
    private final long maxHeapBytes;

    public SystemResources(long freeHeapBytes, long totalHeapBytes, long maxHeapBytes) {
        this.freeHeapBytes = freeHeapBytes;
        this.totalHeapBytes = totalHeapBytes;
        this.maxHeapBytes = maxHeapBytes;
    }

    public long getFreeHeapBytes() { return freeHeapBytes; }
    public long getTotalHeapBytes() { return totalHeapBytes; }
    public long getMaxHeapBytes() { return maxHeapBytes; }

    public long getFreeHeapMiB() { return freeHeapBytes / (1024 * 1024); }
}