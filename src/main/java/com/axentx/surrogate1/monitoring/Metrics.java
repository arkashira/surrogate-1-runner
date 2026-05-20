package com.axentx.surrogate1.monitoring;

/**
 * Immutable snapshot of system metrics.
 */
public final class Metrics {
    private final double cpuUsage;   // percent
    private final double memoryUsage; // percent
    private final double gpuUsage;   // percent

    public Metrics(double cpuUsage, double memoryUsage, double gpuUsage) {
        this.cpuUsage = cpuUsage;
        this.memoryUsage = memoryUsage;
        this.gpuUsage = gpuUsage;
    }

    public double getCpuUsage() {
        return cpuUsage;
    }

    public double getMemoryUsage() {
        return memoryUsage;
    }

    public double getGpuUsage() {
        return gpuUsage;
    }

    @Override
    public String toString() {
        return String.format("CPU: %.1f%%, MEM: %.1f%%, GPU: %.1f%%",
                cpuUsage, memoryUsage, gpuUsage);
    }
}