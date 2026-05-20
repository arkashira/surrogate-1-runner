package com.axentx.surrogate.agent;

import com.axentx.surrogate.config.AgentConfig;
import java.util.Map;

public interface AgentFactory {
    Agent createAgent(AgentConfig config);
}