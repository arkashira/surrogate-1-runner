package com.axentx.surrogate1;

import java.io.IOException;

/**
 * Interface for an LLM provider. Implementations should provide a method
 * to send a prompt to the underlying LLM service and return the response.
 */
public interface LlmProvider {
    /**
     * Sends the given prompt to the LLM provider and returns the response.
     *
     * @param prompt the prompt to send
     * @return the LLM response
     * @throws IOException          if an I/O error occurs
     * @throws InterruptedException if the operation is interrupted
     */
    String getResponse(String prompt) throws IOException, InterruptedException;

    /**
     * Returns a human‑readable name for the provider.
     *
     * @return provider name
     */
    String getName();
}