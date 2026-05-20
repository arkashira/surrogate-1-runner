package com.axentx.surrogate1.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.util.StringUtils;

import java.util.Map;

@Configuration
@PropertySource("classpath:application.yml")
public class LLMConfigLoader {

    @Value("${llm.provider:openai}") // Default to 'openai'
    private String defaultProvider;

    @Value("${llm.providers}")
    private Map<String, String> providerUrls;

    public String getProviderUrl(String envVarName) {
        String envProvider = System.getenv(envVarName);
        if (StringUtils.hasText(envProvider)) {
            return providerUrls.getOrDefault(envProvider, providerUrls.get(defaultProvider));
        }
        return providerUrls.get(defaultProvider);
    }

    public String getDefaultProvider() {
        return defaultProvider;
    }

    public Map<String, String> getProviderUrls() {
        return providerUrls;
    }
}