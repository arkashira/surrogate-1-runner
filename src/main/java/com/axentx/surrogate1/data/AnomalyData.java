package com.axentx.surrogate1.data;

public class AnomalyData {
    private final double usage;
    private final long timestamp;

    public AnomalyData(double usage) {
        this.usage = usage;
        this.timestamp = System.currentTimeMillis();
    }

    public double getUsage() {
        return usage;
    }

    public long getTimestamp() {
        return timestamp;
    }
}