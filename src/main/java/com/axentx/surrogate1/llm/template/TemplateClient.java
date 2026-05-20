package com.axentx.surrogate1.llm.template;

/**
 * TemplateClient is an abstract base class for all LLM provider clients.
 * <p>
 * New providers should extend this class and implement the abstract methods
 * {@link #sendPrompt(String)} and {@link #parseResponse(String)}.  The
 * {@link #configure(ProviderConfig)} method can be overridden to apply
 * provider‑specific configuration.
 *
 * <p>Example implementation:
 * <pre>{@code
 * public class MyProviderClient extends TemplateClient {
 *     @Override
 *     public String sendPrompt(String prompt) throws LLMProviderException {
 *         // call provider API
 *     }
 *
 *     @Override
 *     public ParsedResponse parseResponse(String rawResponse) {
 *         // parse raw JSON, etc.
 *     }
 * }
 * }</pre>
 *
 * @author axentx
 */
public abstract class TemplateClient {

    /**
     * Sends a prompt to the LLM provider and returns the raw response.
     *
     * @param prompt The prompt text.
     * @return The raw response from the provider.
     * @throws LLMProviderException if the provider fails to respond.
     */
    public abstract String sendPrompt(String prompt) throws LLMProviderException;

    /**
     * Parses the raw provider response into a structured format.
     *
     * @param rawResponse The raw response string.
     * @return The parsed response.
     */
    public abstract ParsedResponse parseResponse(String rawResponse);

    /**
     * Optional: configure provider-specific settings.
     *
     * @param config The configuration object.
     */
    public void configure(ProviderConfig config) {
        // Default no‑op implementation.
    }
}