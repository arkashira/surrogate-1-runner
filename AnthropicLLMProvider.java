package com.axentx.surrogate1.provider;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class AnthropicLLMProvider implements LLMProvider {

    @Value("${llm.providers.anthropic}")
    private String apiUrl;

    @Override
    public String generateResponse(String prompt) {
        // Placeholder for Anthropic API integration
        return "Generated response from Anthropic using endpoint: " + apiUrl + "\nPrompt: " + prompt;
    }
}