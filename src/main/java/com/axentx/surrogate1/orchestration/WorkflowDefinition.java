package com.axentx.surrogate1.orchestration;

import java.util.List;
import java.util.Map;

/**
 * WorkflowDefinition defines the structure of a workflow:
 * - A list of child agent roles to delegate to
 * - Parameters for each child agent
 * - Optional metadata for the entire workflow
 */
public class WorkflowDefinition {

    private final List<ChildAgentSpec> childAgents;
    private final Map<String, Object> workflowMetadata;

    public WorkflowDefinition(List<ChildAgentSpec> childAgents,
                              Map<String, Object> workflowMetadata) {
        this.childAgents = childAgents;
        this.workflowMetadata = workflowMetadata;
    }

    public List<ChildAgentSpec> getChildAgents() {
        return childAgents;
    }

    public Map<String, Object> getWorkflowMetadata() {
        return workflowMetadata;
    }

    /**
     * ChildAgentSpec encapsulates a single child agent's role and its parameters.
     */
    public static class ChildAgentSpec {
        private final String role;
        private final Map<String, Object> parameters;

        public ChildAgentSpec(String role, Map<String, Object> parameters) {
            this.role = role;
            this.parameters = parameters;
        }

        public String getRole() {
            return role;
        }

        public Map<String, Object> getParameters() {
            return parameters;
        }
    }
}