package com.axentx.surrogate.agent;

import java.util.List;

public class AgentHierarchy {
    private Agent rootAgent;
    private List<Agent> childAgents;

    public AgentHierarchy(Agent rootAgent) {
        this.rootAgent = rootAgent;
        this.childAgents = rootAgent.getChildAgents();
    }

    public Agent getRootAgent() {
        return rootAgent;
    }

    public List<Agent> getChildAgents() {
        return childAgents;
    }

    public void addChildAgent(Agent agent) {
        rootAgent.addChildAgent(agent);
        childAgents = rootAgent.getChildAgents();
    }

    public void removeChildAgent(Agent agent) {
        rootAgent.removeChildAgent(agent);
        childAgents = rootAgent.getChildAgents();
    }
}