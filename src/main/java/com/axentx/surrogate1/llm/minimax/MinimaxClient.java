package com.axentx.surrogate1.llm.minimax;

import com.axentx.surrogate1.llm.LLMClient;
import com.axentx.surrogate1.llm.LLMConfig;
import com.axentx.surrogate1.llm.LLMResponse;
import com.axentx.surrogate1.llm.LLMRequest;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class MinimaxClient implements LLMClient {

    private static final String BASE_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2";
    private static final String API_VERSION = "2024-01-15";
    private static final ObjectMapper MAPPER = new ObjectMapper();

    private final String apiKey;
    private final String model;
    private final CloseableHttpClient httpClient;

    public MinimaxClient(LLMConfig config) {
        this.apiKey = config.getApiKey();
        this.model = config.getModel();
        this.httpClient = createHttpClient();
    }

    private CloseableHttpClient createHttpClient() {
        RequestConfig requestConfig = RequestConfig.custom()
                .setConnectTimeout(30, TimeUnit.SECONDS)
                .setSocketTimeout(60, TimeUnit.SECONDS)
                .setConnectionRequestTimeout(30, TimeUnit.SECONDS)
                .build();

        return HttpClients.custom()
                .setDefaultRequestConfig(requestConfig)
                .build();
    }

    @Override
    public LLMResponse chat(LLMRequest request) throws IOException {
        String requestBody = buildRequestBody(request);
        String responseJson = sendRequest(requestBody);
        return parseResponse(responseJson);
    }

    private String buildRequestBody(LLMRequest request) {
        ObjectNode root = MAPPER.createObjectNode();
        root.put("model", model);
        root.put("api_key", apiKey);
        root.put("prompt", request.getMessages().stream()
                .map(msg -> formatMessage(msg))
                .reduce("", (acc, msg) -> acc + "\n" + msg));
        root.put("temperature", request.getTemperature());
        root.put("top_p", request.getTopP());
        root.put("top_k", request.getTopK());
        root.put("max_tokens", request.getMaxTokens());
        root.put("stop", request.getStopSequences());
        root.put("n", request.getN());
        root.put("presence_penalty", request.getPresencePenalty());
        root.put("frequency_penalty", request.getFrequencyPenalty());

        return root.toString();
    }

    private String formatMessage(com.axentx.surrogate1.llm.Message msg) {
        String role = msg.getRole();
        String content = msg.getContent();

        if ("system".equalsIgnoreCase(role)) {
            return "system: " + content;
        } else if ("user".equalsIgnoreCase(role)) {
            return "user: " + content;
        } else if ("assistant".equalsIgnoreCase(role)) {
            return "assistant: " + content;
        } else {
            return "user: " + content;
        }
    }

    private String sendRequest(String requestBody) throws IOException {
        HttpPost post = new HttpPost(BASE_URL);
        post.setHeader("Content-Type", "application/json");
        post.setHeader("Authorization", "Bearer " + apiKey);

        StringEntity entity = new StringEntity(requestBody, "UTF-8");
        post.setEntity(entity);

        try (CloseableHttpResponse response = httpClient.execute(post)) {
            return EntityUtils.toString(response.getEntity());
        }
    }

    private LLMResponse parseResponse(String responseJson) throws IOException {
        JsonNode rootNode = MAPPER.readTree(responseJson);
        
        String content = rootNode.has("choices") && rootNode.get("choices").isArray()
                ? rootNode.get("choices").get(0).get("message").get("content").asText()
                : "";

        long finishTime = System.currentTimeMillis();
        
        return LLMResponse.builder()
                .content(content)
                .finishTime(finishTime)
                .usage(parseUsage(rootNode))
                .build();
    }

    private Map<String, Integer> parseUsage(JsonNode rootNode) {
        Map<String, Integer> usage = new HashMap<>();
        JsonNode usageNode = rootNode.has("usage") ? rootNode.get("usage") : null;
        
        if (usageNode != null) {
            usage.put("prompt_tokens", usageNode.has("prompt_tokens") ? usageNode.get("prompt_tokens").asInt() : 0);
            usage.put("completion_tokens", usageNode.has("completion_tokens") ? usageNode.get("completion_tokens").asInt() : 0);
            usage.put("total_tokens", usageNode.has("total_tokens") ? usageNode.get("total_tokens").asInt() : 0);
        }
        
        return usage;
    }

    @Override
    public List<String> getSupportedModels() {
        return List.of(
            "abab5.5s",
            "abab6s",
            "abab6.5s",
            "abab6.5t",
            "abab6.5t-chat",
            "abab6.5t-chat-2407",
            "abab6.5t-chat-2407-128k"
        );
    }

    @Override
    public String getProvider() {
        return "minimax";
    }

    @Override
    public void close() throws IOException {
        if (httpClient != null) {
            httpClient.close();
        }
    }
}