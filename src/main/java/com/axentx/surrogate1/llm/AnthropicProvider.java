package com.axentx.surrogate1.llm;

/**
 * Anthropic provider implementation.
 */
public class AnthropicProvider implements LLMProvider {
    @Override
    public String getName() {
        return "Anthropic";
    }

    @Override
    public String generate(String prompt) {
        // Stub implementation – in production this would call the Anthropic API
        return "Anthropic response to: " + prompt;
    }
}