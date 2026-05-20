package com.axentx.surrogate1;

import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Orchestrates calls to multiple LLM providers. Providers are selected
 * in a round‑robin fashion. The orchestrator retries a failed call
 * up to {@code maxRetries} times before propagating the exception.
 */
public class LlmOrchestrator {
    private final List<LlmProvider> providers;
    private final AtomicInteger counter = new AtomicInteger(0);
    private final int maxRetries;

    /**
     * Creates an orchestrator with the given providers.
     *
     * @param providers list of providers to use
     * @param maxRetries maximum number of retries per request
     */
    public LlmOrchestrator(List<LlmProvider> providers, int maxRetries) {
        if (providers == null || providers.isEmpty()) {
            throw new IllegalArgumentException("At least one provider must be supplied");
        }
        this.providers = providers;
        this.maxRetries = maxRetries;
    }

    /**
     * Sends the prompt to the next provider in the round‑robin cycle.
     *
     * @param prompt the prompt to send
     * @return the provider's response
     * @throws Exception if all retries fail
     */
    public String orchestrate(String prompt) throws Exception {
        int attempts = 0;
        while (attempts < maxRetries) {
            LlmProvider provider = getNextProvider();
            try {
                return provider.getResponse(prompt);
            } catch (Exception e) {
                attempts++;
                // Simple back‑off: log and retry
                System.err.println("Provider " + provider.getName() + " failed (attempt " + attempts + "): " + e.getMessage());
                if (attempts >= maxRetries) {
                    throw new Exception("All retries failed for prompt: " + prompt, e);
                }
            }
        }
        throw new Exception("Unexpected error in orchestrate");
    }

    private LlmProvider getNextProvider() {
        int index = Math.abs(counter.getAndIncrement() % providers.size());
        return providers.get(index);
    }
}