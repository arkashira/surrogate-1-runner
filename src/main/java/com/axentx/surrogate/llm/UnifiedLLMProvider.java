package com.axentx.surrogate.llm;

import java.util.Map;

/**
 * Unified interface for LLM providers.
 *
 * <p>This interface abstracts provider-specific quirks and provides a consistent
 * API for sending prompts and receiving completions. Implementations should
 * support at least two popular providers (e.g., OpenAI and Anthropic).
 */
public interface UnifiedLLMProvider {

    /**
     * Sends a prompt to the LLM provider and returns the generated text.
     *
     * @param prompt The input prompt to send.
     * @param parameters Optional provider-specific parameters (e.g., temperature,
     *                   maxTokens). Keys are provider-agnostic where possible.
     * @return The LLM's completion text.
     * @throws LLMException if the provider returns an error or the request fails.
     */
    String complete(String prompt, Map<String, Object> parameters) throws LLMException;

    /**
     * Returns the name of the underlying provider (e.g., "openai", "anthropic").
     *
     * @return Provider name.
     */
    String getProviderName();
}