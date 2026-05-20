package com.axentx.surrogate1.monitoring;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * MonitoringSystem provides real‑time monitoring of AI/ML workloads.
 *
 * <p>The system periodically collects system metrics (CPU, memory, GPU) and notifies a
 * {@link MonitoringListener}.  The polling interval can be adapted at runtime based on
 * observed workload characteristics.</p>
 *
 * <p>Typical usage:</p>
 * <pre>{@code
 * MonitoringListener listener = metrics -> System.out.println("Metrics: " + metrics);
 * MonitoringSystem monitor = new MonitoringSystem(listener, 5_000);
 * monitor.start();
 * // ... run workload ...
 * monitor.stop();
 * }</pre>
 */
public class MonitoringSystem {

    private final ScheduledExecutorService scheduler;
    private final MonitoringListener listener;
    private volatile long intervalMs;
    private volatile boolean running = false;

    // Thresholds for adaptive interval adjustment
    private static final double CPU_HIGH_THRESHOLD = 80.0; // percent
    private static final double CPU_LOW_THRESHOLD = 20.0;  // percent
    private static final long MIN_INTERVAL_MS = 1_000;
    private static final long MAX_INTERVAL_MS = 30_000;

    /**
     * Creates a MonitoringSystem.
     *
     * @param listener   callback invoked with collected metrics
     * @param intervalMs initial polling interval in milliseconds
     */
    public MonitoringSystem(MonitoringListener listener, long intervalMs) {
        this.listener = listener;
        this.intervalMs = intervalMs;
        this.scheduler = Executors.newSingleThreadScheduledExecutor(r -> {
            Thread t = new Thread(r, "MonitoringSystem-Thread");
            t.setDaemon(true);
            return t;
        });
    }

    /**
     * Starts monitoring.  If already running, this is a no‑op.
     */
    public synchronized void start() {
        if (running) {
            return;
        }
        running = true;
        scheduler.scheduleAtFixedRate(this::pollMetrics, 0, intervalMs, TimeUnit.MILLISECONDS);
    }

    /**
     * Stops monitoring and shuts down the scheduler.
     */
    public synchronized void stop() {
        if (!running) {
            return;
        }
        running = false;
        scheduler.shutdownNow();
    }

    /**
     * Polls system metrics and notifies the listener.  Also adapts the polling interval
     * based on CPU usage.
     */
    private void pollMetrics() {
        Metrics metrics = collectMetrics();
        listener.onMetrics(metrics);
        adaptInterval(metrics);
    }

    /**
     * Collects current system metrics.  In a real implementation this would query OS
     * APIs or a monitoring agent.  Here we provide a lightweight stub that simulates
     * varying values for demonstration purposes.
     *
     * @return current metrics snapshot
     */
    private Metrics collectMetrics() {
        // Simulate CPU usage oscillation
        double cpu = 20 + Math.random() * 60; // 20% to 80%
        double memory = 30 + Math.random() * 50; // 30% to 80%
        double gpu = 10 + Math.random() * 70; // 10% to 80%
        return new Metrics(cpu, memory, gpu);
    }

    /**
     * Adapts the polling interval based on CPU usage to provide more frequent updates
     * when the workload is heavy and reduce overhead when idle.
     *
     * @param metrics current metrics snapshot
     */
    private void adaptInterval(Metrics metrics) {
        long newInterval = intervalMs;
        if (metrics.getCpuUsage() > CPU_HIGH_THRESHOLD) {
            newInterval = Math.max(MIN_INTERVAL_MS, intervalMs / 2);
        } else if (metrics.getCpuUsage() < CPU_LOW_THRESHOLD) {
            newInterval = Math.min(MAX_INTERVAL_MS, intervalMs * 2);
        }

        if (newInterval != intervalMs) {
            intervalMs = newInterval;
            // Reschedule with new interval
            scheduler.shutdownNow();
            scheduler.scheduleAtFixedRate(this::pollMetrics, 0, intervalMs, TimeUnit.MILLISECONDS);
        }
    }
}