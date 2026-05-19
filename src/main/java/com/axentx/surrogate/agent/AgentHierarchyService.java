package com.axentx.surrogate.agent;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AgentHierarchyService {
    private AgentHierarchy agentHierarchy;

    public AgentHierarchyService() {
        Agent rootAgent = new Agent("root", "Root Agent");
        this.agentHierarchy = new AgentHierarchy(rootAgent);
    }

    public Agent getRootAgent() {
        return agentHierarchy.getRootAgent();
    }

    public List<Agent> getChildAgents() {
        return agentHierarchy.getChildAgents();
    }

    public void addChildAgent(Agent agent) {
        agentHierarchy.addChildAgent(agent);
    }

    public void removeChildAgent(Agent agent) {
        agentHierarchy.removeChildAgent(agent);
    }
}