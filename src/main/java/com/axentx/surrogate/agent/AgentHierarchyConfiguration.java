package com.axentx.surrogate.agent;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AgentHierarchyConfiguration {
    @Bean
    public AgentHierarchyAPI agentHierarchyAPI(AgentHierarchyService agentHierarchyService) {
        return new AgentHierarchyAPI(agentHierarchyService.getAgentHierarchy());
    }

    @Bean
    public AgentHierarchyService agentHierarchyService() {
        return new AgentHierarchyService();
    }
}