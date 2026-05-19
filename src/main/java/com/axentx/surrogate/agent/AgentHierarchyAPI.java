package com.axentx.surrogate.agent;

import java.util.List;

public class AgentHierarchyAPI {
    private AgentHierarchy agentHierarchy;

    public AgentHierarchyAPI(AgentHierarchy agentHierarchy) {
        this.agentHierarchy = agentHierarchy;
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