package com.axentx.surrogate.agent;

import java.util.ArrayList;
import java.util.List;

public class Agent {
    private String id;
    private String name;
    private List<Agent> childAgents;

    public Agent(String id, String name) {
        this.id = id;
        this.name = name;
        this.childAgents = new ArrayList<>();
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<Agent> getChildAgents() {
        return childAgents;
    }

    public void addChildAgent(Agent agent) {
        childAgents.add(agent);
    }

    public void removeChildAgent(Agent agent) {
        childAgents.remove(agent);
    }
}