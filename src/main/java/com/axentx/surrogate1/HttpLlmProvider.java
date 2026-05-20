package com.axentx.surrogate1;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * A simple HTTP based LLM provider that talks to the llm‑orchestra
 * API. The provider expects the endpoint to accept a JSON payload
 * with a single field {@code prompt} and return a JSON payload
 * containing a {@code response} field.
 */
public class HttpLlmProvider implements LlmProvider {
    private final String name;
    private final String endpoint;
    private final HttpClient client = HttpClient.newHttpClient();

    public HttpLlmProvider(String name, String endpoint) {
        this.name = name;
        this.endpoint = endpoint;
    }

    @Override
    public String getResponse(String prompt) throws IOException, InterruptedException {
        String jsonBody = "{\"prompt\":\"" + escapeJson(prompt) + "\"}";
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(endpoint))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new IOException("Non‑200 response (" + response.statusCode() + "): " + response.body());
        }

        // Very naive JSON extraction – assumes the response contains
        // a field named "response" with a string value.
        String body = response.body();
        int idx = body.indexOf("\"response\":\"");
        if (idx == -1) {
            return body; // fallback to raw body
        }
        int start = idx + "\"response\":\"".length();
        int end = body.indexOf("\"", start);
        if (end == -1) {
            return body;
        }
        return body.substring(start, end);
    }

    @Override
    public String getName() {
        return name;
    }

    private String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}