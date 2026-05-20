package com.axentx.surrogate1.llm;

import java.util.HashMap;
import java.util.Map;

public class LLMClientFactory {
    public static LLMClient createClient(String provider, Map<String, Object> config) {
        Map<String, Object> clientConfig = new HashMap<>(config);
        clientConfig.put("provider", provider);
        return new LLMClient(clientConfig);
    }
}