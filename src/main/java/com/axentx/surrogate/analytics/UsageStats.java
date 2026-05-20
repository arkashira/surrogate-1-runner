package com.axentx.surrogate.analytics;

/**
 * Immutable DTO that is sent to the UI (JSON or SSE).
 */
public class UsageStats {
    private final long pipelineCount;
    private final double totalDataMb;
    private final long avgRunTimeMs;

    public UsageStats(long pipelineCount, double totalDataMb, long avgRunTimeMs) {
        this.pipelineCount = pipelineCount;
        this.totalDataMb = totalDataMb;
        this.avgRunTimeMs = avgRunTimeMs;
    }

    public long getPipelineCount() {
        return pipelineCount;
    }

    public double getTotalDataMb() {
        return totalDataMb;
    }

    public long getAvgRunTimeMs() {
        return avgRunTimeMs;
    }
}