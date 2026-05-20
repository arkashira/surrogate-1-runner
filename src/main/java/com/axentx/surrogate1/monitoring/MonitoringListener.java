package com.axentx.surrogate1.monitoring;

/**
 * Callback interface for receiving real‑time metrics from {@link MonitoringSystem}.
 */
public interface MonitoringListener {
    void onMetrics(Metrics metrics);
}