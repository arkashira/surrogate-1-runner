package com.axentx.surrogate1.llm.template;

/**
 * Configuration holder for LLM providers.  Concrete providers can add
 * fields as needed; this base class keeps the API stable.
 */
public class ProviderConfig {
    // Example common config fields
    private String apiKey;
    private String endpoint;

    public ProviderConfig() {}

    public ProviderConfig(String apiKey, String endpoint) {
        this.apiKey = apiKey;
        this.endpoint = endpoint;
    }

    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }

    public String getEndpoint() {
        return endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }
}