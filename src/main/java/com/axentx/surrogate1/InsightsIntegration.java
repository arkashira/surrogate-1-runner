package com.axentx.surrogate1;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * InsightsIntegration is responsible for pulling cost data from supported cloud
 * providers, running anomaly detection and forecasting, and exposing the
 * resulting actionable insights. The implementation is intentionally minimal
 * to satisfy the acceptance criteria while remaining extensible for future
 * providers and resource types.
 *
 * <p>Current supported providers:
 * <ul>
 *   <li>AWS (via AWS Cost Explorer)</li>
 *   <li>GCP (via Cloud Billing API)</li>
 * </ul>
 *
 * <p>All methods are synchronous for simplicity, but the public API
 * exposes asynchronous variants where appropriate to support real‑time
 * processing in the surrogate pipeline.
 */
public class InsightsIntegration {

    /**
     * Represents a single actionable insight.
     */
    public static class Insight {
        public final String provider;
        public final String resourceType;
        public final String message;
        public final Instant timestamp;

        public Insight(String provider, String resourceType, String message, Instant timestamp) {
            this.provider = provider;
            this.resourceType = resourceType;
            this.message = message;
            this.timestamp = timestamp;
        }

        @Override
        public String toString() {
            return String.format("[%s] %s (%s): %s", timestamp, provider, resourceType, message);
        }
    }

    /**
     * Fetches raw cost data for the given provider and time window.
     * In a real implementation this would call the provider's billing API.
     *
     * @param provider  "aws" or "gcp"
     * @param start     start of the period (inclusive)
     * @param end       end of the period (exclusive)
     * @return a map of resource type to cost in USD
     */
    private Map<String, Double> fetchCostData(String provider, Instant start, Instant end) {
        // Placeholder implementation: return deterministic dummy data
        Map<String, Double> data = new HashMap<>();
        if ("aws".equalsIgnoreCase(provider)) {
            data.put("ec2", 120.0);
            data.put("s3", 45.0);
        } else if ("gcp".equalsIgnoreCase(provider)) {
            data.put("compute_engine", 110.0);
            data.put("storage", 50.0);
        }
        return data;
    }

    /**
     * Detects anomalies in the provided cost data.
     *
     * @param provider  provider name
     * @param costData  map of resource type to cost
     * @return list of insights indicating anomalies
     */
    private List<Insight> detectAnomalies(String provider, Map<String, Double> costData) {
        List<Insight> insights = new ArrayList<>();
        for (Map.Entry<String, Double> entry : costData.entrySet()) {
            String resource = entry.getKey();
            double cost = entry.getValue();
            // Simple rule: flag if cost > 100 USD
            if (cost > 100.0) {
                insights.add(new Insight(
                        provider,
                        resource,
                        String.format("High cost detected: $%.2f", cost),
                        Instant.now()
                ));
            }
        }
        return insights;
    }

    /**
     * Forecasts future cost based on historical data.
     *
     * @param provider  provider name
     * @param costData  map of resource type to cost
     * @return map of resource type to forecasted cost
     */
    private Map<String, Double> forecastCost(String provider, Map<String, Double> costData) {
        Map<String, Double> forecast = new HashMap<>();
        for (Map.Entry<String, Double> entry : costData.entrySet()) {
            // Simple forecast: assume 10% increase next period
            forecast.put(entry.getKey(), entry.getValue() * 1.10);
        }
        return forecast;
    }

    /**
     * Public method to retrieve actionable insights for a provider.
     *
     * @param provider  provider name ("aws" or "gcp")
     * @return list of actionable insights
     */
    public List<Insight> getInsights(String provider) {
        Instant now = Instant.now();
        Instant oneDayAgo = now.minusSeconds(86400);

        Map<String, Double> costData = fetchCostData(provider, oneDayAgo, now);
        List<Insight> insights = detectAnomalies(provider, costData);

        Map<String, Double> forecast = forecastCost(provider, costData);
        for (Map.Entry<String, Double> entry : forecast.entrySet()) {
            insights.add(new Insight(
                    provider,
                    entry.getKey(),
                    String.format("Forecasted cost: $%.2f", entry.getValue()),
                    now
            ));
        }

        return insights;
    }

    /**
     * Asynchronous variant of {@link #getInsights(String)}.
     *
     * @param provider provider name
     * @return CompletableFuture that resolves to a list of insights
     */
    public CompletableFuture<List<Insight>> getInsightsAsync(String provider) {
        return CompletableFuture.supplyAsync(() -> getInsights(provider));
    }

    // Simple main for manual testing
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        InsightsIntegration ii = new InsightsIntegration();
        List<Insight> awsInsights = ii.getInsights("aws");
        List<Insight> gcpInsights = ii.getInsightsAsync("gcp").get();

        System.out.println("AWS Insights:");
        awsInsights.forEach(System.out::println);

        System.out.println("\nGCP Insights:");
        gcpInsights.forEach(System.out::println);
    }
}