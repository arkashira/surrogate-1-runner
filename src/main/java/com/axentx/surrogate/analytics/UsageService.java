package com.axentx.surrogate.analytics;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

/**
 * Periodically recomputes usage statistics.
 * Replace the placeholder logic with real queries to your DB / metrics store.
 */
@Service
public class UsageService {

    /** Holds the latest snapshot – read‑only for callers. */
    private volatile UsageStats currentStats = new UsageStats(0, 0.0, 0);

    public UsageStats getCurrentStats() {
        return currentStats;
    }

    /** Runs every minute (configurable) */
    @Scheduled(fixedRateString = "${usage.update-rate-ms:60000}")
    public void refreshStats() {
        // ---- BEGIN: replace with real analytics code ----
        long pipelineCount = fetchPipelineCount();          // e.g. SELECT COUNT(*) FROM pipelines
        double totalDataMb   = fetchTotalDataIngestedMb();   // e.g. SUM(bytes)/1_048_576
        long avgRunTimeMs   = fetchAverageRunTimeMs();       // e.g. AVG(duration_ms)
        // ---- END: real code ----

        this.currentStats = new UsageStats(pipelineCount, totalDataMb, avgRunTimeMs);
    }

    /* -----------------------------------------------------------------
       Stub methods – delete them once you have real data sources.
       ----------------------------------------------------------------- */
    private long fetchPipelineCount() { return 12L; }
    private double fetchTotalDataIngestedMb() { return 842.3; }
    private long fetchAverageRunTimeMs() { return 1345L; }
}