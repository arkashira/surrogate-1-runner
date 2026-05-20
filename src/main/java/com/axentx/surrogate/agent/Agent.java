package com.axentx.surrogate.agent;

import com.axentx.surrogate.config.AgentConfig;
import com.axentx.surrogate.model.AgentResult;
import java.util.Map;

public interface Agent {
    String getName();
    AgentResult execute(Map<String, Object> sharedContext);
}