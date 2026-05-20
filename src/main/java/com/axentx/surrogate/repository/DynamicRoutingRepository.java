package com.axentx.surrogate.repository;

import java.util.ArrayList;
import java.util.List;

public class DynamicRoutingRepository {

    private List<String> agents = new ArrayList<>();

    public List<String> getAvailableAgents() {
        return new ArrayList<>(agents);
    }

    public void addAgent(String agentId) {
        if (!agents.contains(agentId)) {
            agents.add(agentId);
        }
    }

    public void removeAgent(String agentId) {
        agents.remove(agentId);
    }
}