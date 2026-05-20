package com.axentx.surrogate1.llm.claude;

import com.axentx.surrogate1.llm.standard.StandardRequest;
import com.axentx.surrogate1.llm.standard.StandardResponse;
import com.axentx.surrogate1.llm.standard.StandardMessage;
import com.axentx.surrogate1.llm.standard.StandardUsage;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Mapper that translates Claude‑specific request/response objects to the
 * unified {@link StandardRequest}/{@link StandardResponse} format used by the
 * surrogate‑1 codebase.
 *
 * <p>This class supports all major Claude models (opus, sonnet, haiku) and
 * maps Claude‑only parameters to the common fields.</p>
 */
public final class ClaudeMapper {

    private ClaudeMapper() {
        // utility class – no instances
    }

    /**
     * Convert a {@link ClaudeRequest} into a {@link StandardRequest}.
     *
     * @param claudeRequest the Claude‑specific request
     * @return a request in the unified format
     */
    public static StandardRequest toStandardRequest(ClaudeRequest claudeRequest) {
        // Map model name – keep the Claude identifier as‑is; the unified layer
        // treats it as a string model ID.
        String model = mapModelName(claudeRequest.getModel());

        // Convert messages – Claude uses a list of maps with "role" and "content".
        List<StandardMessage> messages = claudeRequest.getMessages()
                .stream()
                .map(m -> new StandardMessage(m.getRole(), m.getContent()))
                .collect(Collectors.toList());

        // Map Claude‑specific parameters to the common ones.
        StandardRequest.StandardRequestBuilder builder = StandardRequest.builder()
                .model(model)
                .messages(messages)
                .temperature(claudeRequest.getTemperature())
                .maxTokens(claudeRequest.getMaxTokens())
                .topP(claudeRequest.getTopP())
                .topK(claudeRequest.getTopK());

        // Claude allows a list of stop sequences; the unified format expects a
        // single comma‑separated string.
        if (claudeRequest.getStopSequences() != null && !claudeRequest.getStopSequences().isEmpty()) {
            builder.stop(String.join(",", claudeRequest.getStopSequences()));
        }

        // Any additional Claude‑only options are stored in the "metadata" map.
        Map<String, Object> metadata = claudeRequest.getMetadata();
        if (metadata != null && !metadata.isEmpty()) {
            builder.metadata(metadata);
        }

        return builder.build();
    }

    /**
     * Convert a {@link ClaudeResponse} into a {@link StandardResponse}.
     *
     * @param claudeResponse the Claude‑specific response
     * @return a response in the unified format
     */
    public static StandardResponse fromClaudeResponse(ClaudeResponse claudeResponse) {
        // Claude returns a list of "completion" objects; we take the first.
        ClaudeResponse.Completion completion = claudeResponse.getCompletion();

        StandardResponse.StandardResponseBuilder builder = StandardResponse.builder()
                .id(claudeResponse.getId())
                .model(mapModelName(claudeResponse.getModel()))
                .content(completion.getText())
                .stopReason(completion.getStopReason());

        // Map usage information with explicit null-check
        ClaudeResponse.Usage usage = claudeResponse.getUsage();
        if (usage != null) {
            StandardUsage standardUsage = StandardUsage.builder()
                    .inputTokens(usage.getInputTokens())
                    .outputTokens(usage.getOutputTokens())
                    .totalTokens(usage.getInputTokens() + usage.getOutputTokens())
                    .build();
            builder.usage(standardUsage);
        }

        // Preserve raw response for extensibility
        builder.rawResponse(claudeResponse.getRaw());

        return builder.build();
    }

    /**
     * Normalise Claude model identifiers to the string used by the unified
     * layer. Currently the unified layer does not enforce a strict enum, so we
     * simply return the identifier unchanged after validating it.
     *
     * @param claudeModel the model name supplied by Claude
     * @return a validated model identifier
     */
    private static String mapModelName(String claudeModel) {
        // Accept known major models; otherwise pass through unchanged.
        switch (claudeModel) {
            case "claude-3-opus-20240229":
            case "claude-3-opus":
                return "claude-3-opus";
            case "claude-3-sonnet-20240229":
            case "claude-3-sonnet":
                return "claude-3-sonnet";
            case "claude-3-haiku-20240307":
            case "claude-3-haiku":
                return "claude-3-haiku";
            default:
                // Allow future model names – they will be handled downstream.
                return claudeModel;
        }
    }
}