package com.axentx.surrogate1.orchestration;

import java.util.List;
import java.util.Map;

public class AgentDelegatorImpl implements AgentDelegator {

    private Map<String, Agent> childAgents;

    public AgentDelegatorImpl() {
        this.childAgents = new HashMap<>();
    }

    public void addChildAgent(String role, Agent agent) {
        childAgents.put(role, agent);
    }

    @Override
    public List<DelegationResult> delegate(WorkflowDefinition workflowDefinition, Map<String, Object> parentContext) {
        List<DelegationResult> results = new ArrayList<>();
        for (ChildAgentSpec childAgentSpec : workflowDefinition.getChildAgents()) {
            String childAgentRole = childAgentSpec.getRole();
            Map<String, Object> childParameters = childAgentSpec.getParameters();
            Agent childAgent = childAgents.get(childAgentRole);
            if (childAgent != null) {
                DelegationResult result = childAgent.execute(childParameters, parentContext);
                results.add(result);
            } else {
                throw new IllegalArgumentException("No child agent found for role: " + childAgentRole);
            }
        }
        return results;
    }

    public static class Agent {
        public DelegationResult execute(Map<String, Object> parameters, Map<String, Object> parentContext) {
            // Execute the task logic here
            System.out.println("Executing task with parameters: " + parameters);
            Map<String, Object> result = new HashMap<>();
            Map<String, Object> metadata = new HashMap<>();
            return new DelegationResult("childAgentRole", parameters, result, metadata);
        }
    }
}