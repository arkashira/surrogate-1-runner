package com.axentx.surrogate.model;

import java.util.List;
import java.util.ArrayList;

public class WorkflowResult {
    private final List<AgentResult> agentResults = new ArrayList<>();

    public void addAgentResult(AgentResult result) {
        agentResults.add(result);
    }

    public List<AgentResult> getAgentResults() {
        return List.copyOf(agentResults);
    }
}