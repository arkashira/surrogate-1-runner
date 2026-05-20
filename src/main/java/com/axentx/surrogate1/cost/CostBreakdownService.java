package com.axentx.surrogate1.cost;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Provides real‑time cost breakdowns by resource type.
 *
 * <p>The service keeps an immutable snapshot in an {@link AtomicReference}.
 * A scheduled task refreshes the snapshot every minute.  The snapshot can
 * also be updated manually via {@link #updateCostBreakdown(String, double)}.</p>
 */
@Service
public class CostBreakdownService {

    /** Latest immutable snapshot of cost data. */
    private final AtomicReference<Map<String, Double>> latestSnapshot =
            new AtomicReference<>(Collections.emptyMap());

    /**
     * Returns the most recent cost breakdown by resource type.
     *
     * @return an immutable copy of the latest snapshot
     */
    public Map<String, Double> getCostBreakdownByResourceType() {
        return latestSnapshot.get();
    }

    /**
     * Returns the total cost across all resource types.
     *
     * @return sum of all costs
     */
    public double getTotalCost() {
        return latestSnapshot.get().values().stream()
                .mapToDouble(Double::doubleValue)
                .sum();
    }

    /**
     * Manually updates a single resource type.  Useful for tests or
     * deterministic data feeds.
     *
     * @param resourceType the key (e.g. "compute")
     * @param cost the new cost
     */
    public void updateCostBreakdown(String resourceType, double cost) {
        // Create a new snapshot that includes the updated value
        Map<String, Double> current = latestSnapshot.get();
        Map<String, Double> updated = new HashMap<>(current);
        updated.put(resourceType, cost);
        latestSnapshot.set(Collections.unmodifiableMap(updated));
    }

    /**
     * Periodically refreshes the cost data.  In a real system this would
     * call an external billing API.  Here we simulate changing costs.
     */
    @Scheduled(fixedRate = 60_000)
    public void refreshCostData() {
        Map<String, Double> newSnapshot = new HashMap<>();
        newSnapshot.put("compute", randomCost(10, 50));
        newSnapshot.put("storage", randomCost(5, 20));
        newSnapshot.put("network", randomCost(2, 10));
        latestSnapshot.set(Collections.unmodifiableMap(newSnapshot));
    }

    private double randomCost(int min, int max) {
        double raw = min + Math.random() * (max - min);
        return Math.round(raw * 100.0) / 100.0;
    }
}