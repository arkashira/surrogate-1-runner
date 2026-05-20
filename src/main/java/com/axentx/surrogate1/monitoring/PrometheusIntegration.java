// File: src/main/java/com/axentx/surrogate1/monitoring/PrometheusIntegration.java
package com.axentx.surrogate1.monitoring;

import io.prometheus.client.Counter;
import io.prometheus.client.Gauge;
import io.prometheus.client.Histogram;
import io.prometheus.client.exporter.HTTPServer;
import io.prometheus.client.hotspot.DefaultExports;

import java.io.IOException;

/**
 * Prometheus integration for Surrogate‑1 drift detection.
 *
 * <p>Exposes the following metrics:
 * <ul>
 *   <li>{@code surrogate1_drift_total} – total number of drift checks performed.</li>
 *   <li>{@code surrogate1_drift_success_total} – number of successful drift checks.</li>
 *   <li>{@code surrogate1_drift_failure_total} – number of failed drift checks.</li>
 *   <li>{@code surrogate1_drift_duration_seconds} – histogram of drift check durations.</li>
 *   <li>{@code surrogate1_drift_current_state} – gauge (0 = no drift, 1 = drift).</li>
 * </ul>
 *
 * <p>The HTTP endpoint is started by {@link #start()} and can be stopped with {@link #stop()}.
 */
public class PrometheusIntegration {

    private static final String METRIC_PREFIX = "surrogate1_drift_";

    // Counters
    private static final Counter driftTotal = Counter.build()
            .name(METRIC_PREFIX + "total")
            .help("Total number of drift checks performed.")
            .register();

    private static final Counter driftSuccessTotal = Counter.build()
            .name(METRIC_PREFIX + "success_total")
            .help("Total number of successful drift checks.")
            .register();

    private static final Counter driftFailureTotal = Counter.build()
            .name(METRIC_PREFIX + "failure_total")
            .help("Total number of failed drift checks.")
            .register();

    // Histogram for duration
    private static final Histogram driftDuration = Histogram.build()
            .name(METRIC_PREFIX + "duration_seconds")
            .help("Histogram of drift check durations in seconds.")
            .buckets(0.1, 0.5, 1, 2, 5, 10, 30, 60)
            .register();

    // Gauge for current state
    private static final Gauge currentState = Gauge.build()
            .name(METRIC_PREFIX + "current_state")
            .help("Current drift state: 0 = no drift, 1 = drift.")
            .register();

    private HTTPServer server;

    /**
     * Starts the Prometheus HTTP server on the configured port.
     *
     * @throws IOException if the server cannot be started
     */
    public synchronized void start() throws IOException {
        // Expose JVM metrics
        DefaultExports.initialize();

        int port = getPortFromEnv();
        server = new HTTPServer(port);
    }

    /**
     * Stops the Prometheus HTTP server.
     */
    public synchronized void stop() {
        if (server != null) {
            server.stop();
            server = null;
        }
    }

    /**
     * Records a single drift check event.
     *
     * @param success      true if the drift check succeeded, false otherwise
     * @param durationMs   duration of the check in milliseconds
     */
    public synchronized void recordDriftCheck(boolean success, long durationMs) {
        driftTotal.inc();
        if (success) {
            driftSuccessTotal.inc();
        } else {
            driftFailureTotal.inc();
        }
        driftDuration.observe(durationMs / 1000.0);
    }

    /**
     * Updates the current drift state gauge.
     *
     * @param drift true if drift is currently detected, false otherwise
     */
    public synchronized void setCurrentState(boolean drift) {
        currentState.set(drift ? 1 : 0);
    }

    /* ------------------------------------------------------------------ */
    /*  Helpers for unit‑testing – package‑private accessors             */
    /* ------------------------------------------------------------------ */

    Counter getDriftTotal() { return driftTotal; }
    Counter getDriftSuccessTotal() { return driftSuccessTotal; }
    Counter getDriftFailureTotal() { return driftFailureTotal; }
    Histogram getDriftDuration() { return driftDuration; }
    Gauge getCurrentState() { return currentState; }

    /* ------------------------------------------------------------------ */
    /*  Private helpers                                                  */
    /* ------------------------------------------------------------------ */

    private int getPortFromEnv() {
        String envPort = System.getenv("PROMETHEUS_PORT");
        if (envPort != null) {
            try {
                return Integer.parseInt(envPort);
            } catch (NumberFormatException ignored) {
            }
        }
        return 9091; // default port
    }
}