package com.axentx.surrogate1.llm;

/**
 * Groq provider implementation.
 */
public class GroqProvider implements LLMProvider {
    @Override
    public String getName() {
        return "Groq";
    }

    @Override
    public String generate(String prompt) {
        // Stub implementation – in production this would call the Groq API
        return "Groq response to: " + prompt;
    }
}