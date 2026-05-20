package com.axentx.surrogate.config;

import java.util.Map;

public record AgentConfig(
        String name,
        String type,
        Map<String, Object> params,
        int timeoutSeconds,
        int retryCount
) {}