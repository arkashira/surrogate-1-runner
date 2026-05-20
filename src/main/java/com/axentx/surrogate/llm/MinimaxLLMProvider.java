package com.axentx.surrogate.llm;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.CompletableFuture;

import okhttp3.*;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Unified implementation of the Minimax LLM provider.
 * Supports a single chat completion endpoint with real-API and dummy fallback logic.
 */
public class MinimaxLLMProvider implements LLMProvider {

    private static final String DEFAULT_ENDPOINT = "https://api.minimax.chat/v1/text/chatcompletion";
    private static final String API_URL = "https://api.minimax.chat/v1/chat/completions";
    private final String apiKey;
    private final HttpClient httpClient;
    private final OkHttpClient client;
    private final ObjectMapper mapper = new ObjectMapper();

    public MinimaxLLMProvider() {
        this.apiKey = System.getenv("MINIMAX_API_KEY");
        this.httpClient = HttpClient.newHttpClient();
        this.client = new OkHttpClient();
    }

    @Override
    public String getName() {
        return "minimax";
    }

    @Override
    public String generate(String prompt) {
        Objects.requireNonNull(prompt, "prompt must not be null");

        // Offline / test mode – no API key → deterministic stub
        if (apiKey == null || apiKey.isBlank()) {
            return "dummy response for prompt: " + prompt;
        }

        // Build a very small request payload accepted by Minimax.
        // The exact schema may evolve; this is sufficient for proof‑of‑concept.
        String jsonPayload = """
                {
                  "model": "abab5.5-chat",
                  "messages": [
                    {"role": "user", "content": "%s"}
                  ]
                }
                """.formatted(escapeJson(prompt));

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(DEFAULT_ENDPOINT))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .build();

        try {
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            int status = response.statusCode();
            if (status >= 200 && status < 300) {
                // In a real implementation we would parse the JSON response.
                // For now we return the raw body.
                return response.body();
            } else {
                throw new RuntimeException("Minimax API error: HTTP " + status + " – " + response.body());
            }
        } catch (IOException | InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Failed to call Minimax API", e);
        }
    }

    @Override
    public CompletableFuture<String> chatCompletion(String prompt) {
        return CompletableFuture.supplyAsync(() -> generate(prompt));
    }

    /**
     * Very small JSON escaper for the prompt string.
     */
    private static String escapeJson(String s) {
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r");
    }
}