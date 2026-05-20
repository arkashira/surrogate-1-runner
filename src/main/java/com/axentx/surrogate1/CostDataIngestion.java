// ───────────────────────────────────────────────────────────────────────────────
//  src/main/java/com/axentx/surrogate/CostDataIngestion.java
// ───────────────────────────────────────────────────────────────────────────────
package com.axentx.surrogate;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Real‑time ingestion of cost data from supported cloud providers.
 *
 * <p>Each provider is polled every {@code pollInterval} (default 1 min) and the
 * retrieved cost records are forwarded to the {@link CostAnomalyDetector}
 * for analysis.</p>
 *
 * <p>To add a new provider simply implement {@link CloudProviderClient} and
 * pass an instance to the constructor.</p>
 */
public class CostDataIngestion {

    private final ScheduledExecutorService scheduler;
    private final List<CloudProviderClient> clients;
    private final CostAnomalyDetector detector;
    private final Duration pollInterval;

    /**
     * @param clients       list of provider clients to poll
     * @param detector      anomaly detector to receive cost records
     * @param pollInterval  how often to poll each provider
     */
    public CostDataIngestion(List<CloudProviderClient> clients,
                             CostAnomalyDetector detector,
                             Duration pollInterval) {
        this.clients = clients;
        this.detector = detector;
        this.pollInterval = pollInterval;
        this.scheduler = Executors.newScheduledThreadPool(clients.size());
    }

    /** Starts the ingestion loop. */
    public void start() {
        for (CloudProviderClient client : clients) {
            scheduler.scheduleAtFixedRate(
                    () -> pollProvider(client),
                    0,
                    pollInterval.toMillis(),
                    TimeUnit.MILLISECONDS);
        }
    }

    /** Stops the ingestion loop gracefully. */
    public void stop() {
        scheduler.shutdown();
        try {
            if (!scheduler.awaitTermination(10, TimeUnit.SECONDS)) {
                scheduler.shutdownNow();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            scheduler.shutdownNow();
        }
    }

    private void pollProvider(CloudProviderClient client) {
        try {
            Instant now = Instant.now();
            List<CostRecord> records = client.fetchCostRecords(now.minus(pollInterval));
            detector.processRecords(records);
        } catch (Exception e) {
            // Replace with a proper logger
            System.err.println("Error polling provider " + client.getProviderName()
                    + ": " + e.getMessage());
        }
    }

    // ───────────────────────────────────────────────────────────────────────────────
    //  Supporting interfaces & POJOs
    // ───────────────────────────────────────────────────────────────────────────────

    /** Interface for cloud provider clients. */
    public interface CloudProviderClient {
        String getProviderName();
        List<CostRecord> fetchCostRecords(Instant since);
    }

    /** Simple POJO representing a cost record. */
    public static final class CostRecord {
        public final String provider;
        public final String resourceType;
        public final String resourceId;
        public final double cost;
        public final Instant timestamp;

        public CostRecord(String provider, String resourceType, String resourceId,
                          double cost, Instant timestamp) {
            this.provider = provider;
            this.resourceType = resourceType;
            this.resourceId = resourceId;
            this.cost = cost;
            this.timestamp = timestamp;
        }
    }

    /** Detector that receives cost records and runs anomaly detection. */
    public interface CostAnomalyDetector {
        void processRecords(List<CostRecord> records);
    }
}