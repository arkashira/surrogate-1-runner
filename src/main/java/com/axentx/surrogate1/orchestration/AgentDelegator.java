package com.axentx.surrogate1.orchestration;

import java.util.List;
import java.util.Map;

/**
 * AgentDelegator is responsible for delegating work to child agents.
 * It preserves context and aggregates results with metadata.
 */
public interface AgentDelegator {

    /**
     * Delegates a list of subtasks to the specified child agents.
     *
     * @param workflowDefinition the workflow definition containing child agent roles and parameters
     * @param parentContext      a map of context key/value pairs to be passed to child agents
     * @return a list of DelegationResult objects containing child agent responses and metadata
     */
    List<DelegationResult> delegate(WorkflowDefinition workflowDefinition, Map<String, Object> parentContext);

    /**
     * Represents the result of a single child agent delegation.
     */
    class DelegationResult {
        private final String childAgentRole;
        private final Map<String, Object> childParameters;
        private final Map<String, Object> result;
        private final Map<String, Object> metadata;

        public DelegationResult(String childAgentRole,
                                Map<String, Object> childParameters,
                                Map<String, Object> result,
                                Map<String, Object> metadata) {
            this.childAgentRole = childAgentRole;
            this.childParameters = childParameters;
            this.result = result;
            this.metadata = metadata;
        }

        public String getChildAgentRole() {
            return childAgentRole;
        }

        public Map<String, Object> getChildParameters() {
            return childParameters;
        }

        public Map<String, Object> getResult() {
            return result;
        }

        public Map<String, Object> getMetadata() {
            return metadata;
        }
    }
}