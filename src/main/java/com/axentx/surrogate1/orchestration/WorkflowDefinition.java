package com.axentx.surrogate1.orchestration;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Represents a workflow definition consisting of a root agent node.
 *
 * <p>The workflow can be validated to ensure all required agents are present
 * and that the hierarchy is well-formed.</p>
 */
public class WorkflowDefinition {

    private final String workflowId;
    private final AgentNode root;

    public WorkflowDefinition(String workflowId, AgentNode root) {
        this.workflowId = Objects.requireNonNull(workflowId, "workflowId must not be null");
        this.root = Objects.requireNonNull(root, "root agent node must not be null");
    }

    public String getWorkflowId() {
        return workflowId;
    }

    public AgentNode getRoot() {
        return root;
    }

    /**
     * Returns a flattened list of all agent nodes in the workflow.
     *
     * @return unmodifiable list of all nodes
     */
    public List<AgentNode> getAllNodes() {
        List<AgentNode> all = new ArrayList<>();
        traverse(root, all);
        return Collections.unmodifiableList(all);
    }

    private void traverse(AgentNode node, List<AgentNode> accumulator) {
        accumulator.add(node);
        for (AgentNode child : node.getChildren()) {
            traverse(child, accumulator);
        }
    }

    /**
     * Validates the entire workflow hierarchy.
     *
     * @throws IllegalStateException if validation fails
     */
    public void validate() {
        root.validate();
    }

    @Override
    public String toString() {
        return "WorkflowDefinition{workflowId='" + workflowId + "', root=" + root + "}";
    }
}