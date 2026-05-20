package com.axentx.surrogate1.llm;

/**
 * Interface for LLM provider implementations.
 */
public interface LLMProvider {
    /**
     * Returns the provider name.
     */
    String getName();

    /**
     * Generates a response for the given prompt.
     *
     * @param prompt the input prompt
     * @return the generated response
     */
    String generate(String prompt);
}