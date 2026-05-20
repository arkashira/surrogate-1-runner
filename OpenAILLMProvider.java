package com.axentx.surrogate1.provider;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class OpenAILLMProvider implements LLMProvider {

    @Value("${llm.providers.openai}")
    private String apiUrl;

    @Override
    public String generateResponse(String prompt) {
        // Example placeholder for actual HTTP call to OpenAI
        return "Generated response from OpenAI using endpoint: " + apiUrl + "\nPrompt: " + prompt;
    }
}