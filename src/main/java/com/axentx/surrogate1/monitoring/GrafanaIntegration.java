package com.axentx.surrogate1.monitoring;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Map;
import java.util.Objects;

/**
 * Simple integration with Grafana alerting via the Grafana HTTP API.
 *
 * <p>This class provides a minimal wrapper around the Grafana Alertmanager API
 * (the same endpoint used by Grafana for alert notifications). It supports
 * posting alerts with a configurable set of labels and annotations, and
 * can be extended to support multiple notification channels by adding
 * additional HTTP endpoints or by using Grafana's built‑in notification
 * channel configuration.
 *
 * <p>Usage example:
 * <pre>{@code
 * GrafanaIntegration grafana = new GrafanaIntegration(
 *     "http://grafana.example.com/api/alertmanager/generic-notifications",
 *     "my-grafana-api-key");
 *
 * Map<String, String> labels = Map.of("severity", "critical", "service", "surrogate-1");
 * Map<String, String> annotations = Map.of("summary", "Drift detected", "description", "Drift threshold exceeded");
 *
 * grafana.postAlert("Surrogate-1 Drift Alert", labels, annotations);
 * }</pre>
 *
 * <p>Note: This implementation uses Java 11+ HttpClient. No external
 * dependencies are required.
 */
public class GrafanaIntegration {

    private final HttpClient httpClient;
    private final URI apiEndpoint;
    private final String apiKey;

    /**
     * Creates a new GrafanaIntegration instance.
     *
     * @param apiEndpoint the full URL to the Grafana alerting endpoint
     * @param apiKey      the API key or bearer token used for authentication
     */
    public GrafanaIntegration(String apiEndpoint, String apiKey) {
        this.apiEndpoint = Objects.requireNonNull(URI.create(apiEndpoint), "apiEndpoint");
        this.apiKey = Objects.requireNonNull(apiKey, "apiKey");
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
    }

    /**
     * Posts an alert to Grafana.
     *
     * @param title       the title of the alert
     * @param labels      key/value pairs that will be added as labels
     * @param annotations key/value pairs that will be added as annotations
     * @throws IOException          if the HTTP request fails
     * @throws InterruptedException if the request is interrupted
     */
    public void postAlert(String title, Map<String, String> labels, Map<String, String> annotations)
            throws IOException, InterruptedException {

        String payload = buildPayload(title, labels, annotations);
        HttpRequest request = HttpRequest.newBuilder()
                .uri(apiEndpoint)
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(payload))
                .build();

        try {
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 400) {
                throw new RuntimeException("Grafana alert failed: " + response.body());
            }
        } catch (Exception e) {
            throw new RuntimeException("Grafana communication error", e);
        }
    }

    private String buildPayload(String title, Map<String, String> labels, Map<String, String> annotations) {
        JsonObject payload = new JsonObject();
        payload.addProperty("title", title);
        payload.add("labels", JsonParser.parseString(labels.toString()).getAsJsonObject());
        payload.add("annotations", JsonParser.parseString(annotations.toString()).getAsJsonObject());

        return payload.toString();
    }

    public static void main(String[] args) {
        // Example usage
        GrafanaIntegration grafana = new GrafanaIntegration(
            "https://grafana.axentx.com/api/alertmanager/generic-notifications",
            "abc123-secret-key"
        );

        Map<String, String> labels = Map.of("severity", "critical", "service", "surrogate-1");
        Map<String, String> annotations = Map.of("summary", "Drift detected", "description", "Drift threshold exceeded");

        grafana.postAlert(
            "Surrogate-1 Drift Alert",
            labels,
            annotations
        );
    }
}