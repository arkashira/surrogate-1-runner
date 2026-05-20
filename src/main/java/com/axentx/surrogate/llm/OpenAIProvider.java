package com.axentx.surrogate.llm;

import java.util.Map;
import java.util.Objects;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

/**
 * OpenAI provider implementation using the Chat Completions API.
 */
public class OpenAIProvider implements UnifiedLLMProvider {

    private static final String ENDPOINT = "https://api.openai.com/v1/chat/completions";
    private final String apiKey;
    private final HttpClient client;
    private final ObjectMapper mapper = new ObjectMapper();
    private String model;

    public OpenAIProvider(String apiKey) {
        this(apiKey, "gpt-4o-mini");
    }

    public OpenAIProvider(String apiKey, String model) {
        this.apiKey = Objects.requireNonNull(apiKey, "API key must not be null");
        this.model = Objects.requireNonNull(model, "Model must not be null");
        this.client = HttpClient.newHttpClient();
    }

    @Override
    public String complete(String prompt, Map<String, Object> parameters) throws LLMException {
        try {
            ObjectNode body = mapper.createObjectNode();
            body.put("model", model);
            body.put("temperature", parameters.getOrDefault("temperature", 0.7));
            body.put("max_tokens", parameters.getOrDefault("maxTokens", 256));
            
            ObjectNode messages = mapper.createObjectNode();
            messages.put("role", "user");
            messages.put("content", prompt);
            body.set("messages", mapper.createArrayNode().add(messages));

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(ENDPOINT))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
                .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() != 200) {
                throw new LLMException("OpenAI error (HTTP " + response.statusCode() + "): " + response.body());
            }

            ObjectNode json = (ObjectNode) mapper.readTree(response.body());
            return json.at("/choices/0/message/content").asText();
        } catch (LLMException e) {
            throw e;
        } catch (Exception e) {
            throw new LLMException("OpenAI request failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String getProviderName() {
        return "openai";
    }
}