package com.axentx.surrogate1.llm;

/**
 * OpenAI provider implementation.
 */
public class OpenAIProvider implements LLMProvider {
    @Override
    public String getName() {
        return "OpenAI";
    }

    @Override
    public String generate(String prompt) {
        // Stub implementation – in production this would call the OpenAI API
        return "OpenAI response to: " + prompt;
    }
}