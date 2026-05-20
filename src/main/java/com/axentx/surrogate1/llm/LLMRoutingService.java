package com.axentx.surrogate1.llm;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Service responsible for routing LLM requests to the configured provider.
 *
 * <p>Provider selection is driven by the {@code LLM_PROVIDER} environment variable.
 * Supported values (case-insensitive):
 * <ul>
 *   <li>{@code OPENAI} - default provider</li>
 *   <li>{@code ANTHROPIC} - Anthropic Claude</li>
 *   <li>{@code GROQ} - Groq Llama3</li>
 *   <li>{@code GOOGLE} - Google Gemini</li>
 *   <li>{@code MISTRAL} - Mistral AI</li>
 *   <li>{@code COHERE} - Cohere</li>
 * </ul>
 *
 * <p>Runtime switching is supported via {@link #setProvider(String)}. The service
 * maintains a thread-safe cache of provider instances.
 */
public class LLMRoutingService {

    public enum Provider {
        OPENAI,
        ANTHROPIC,
        GROQ,
        GOOGLE,
        MISTRAL,
        COHERE
    }

    private static final String ENV_VAR = "LLM_PROVIDER";
    private static final Provider DEFAULT_PROVIDER = Provider.OPENAI;

    private final Map<Provider, LLMProvider> providerCache = new ConcurrentHashMap<>();
    private volatile Provider currentProvider;

    public LLMRoutingService() {
        String env = System.getenv(ENV_VAR);
        if (env != null && !env.isBlank()) {
            try {
                currentProvider = Provider.valueOf(env.trim().toUpperCase());
            } catch (IllegalArgumentException e) {
                currentProvider = DEFAULT_PROVIDER;
            }
        } else {
            currentProvider = DEFAULT_PROVIDER;
        }
    }

    /**
     * Returns the current provider instance.
     */
    public LLMProvider getProvider() {
        return providerCache.computeIfAbsent(currentProvider, this::createProvider);
    }

    /**
     * Returns the current provider name.
     */
    public String getProviderName() {
        return currentProvider.name();
    }

    /**
     * Switches the active provider at runtime.
     *
     * @param providerName name of the provider (case-insensitive)
     * @throws IllegalArgumentException if providerName is unsupported
     */
    public void setProvider(String providerName) {
        if (providerName == null || providerName.isBlank()) {
            throw new IllegalArgumentException("Provider name cannot be null or empty");
        }
        Provider newProvider = Provider.valueOf(providerName.trim().toUpperCase());
        currentProvider = newProvider;
    }

    /**
     * Returns all supported providers.
     */
    public Provider[] getSupportedProviders() {
        return Provider.values();
    }

    private LLMProvider createProvider(Provider provider) {
        return switch (provider) {
            case OPENAI -> new OpenAIProvider();
            case ANTHROPIC -> new AnthropicProvider();
            case GROQ -> new GroqProvider();
            case GOOGLE -> new GoogleProvider();
            case MISTRAL -> new MistralProvider();
            case COHERE -> new CohereProvider();
        };
    }
}