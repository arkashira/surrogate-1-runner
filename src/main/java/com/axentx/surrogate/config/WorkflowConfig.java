package com.axentx.surrogate.config;

import java.util.List;

public record WorkflowConfig(
        List<AgentConfig> agents
) {}