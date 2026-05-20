package com.axentx.surrogate.workflow;

/**
 * Represents the lifecycle state of an automated workflow.
 *
 * <p>States are intentionally limited to a small set to keep the manager lightweight
 * while still conveying the essential progress information to the caller.</p>
 */
public enum WorkflowStatus {
    /** Workflow has been created but not yet started. */
    PENDING,

    /** Workflow is currently executing. */
    RUNNING,

    /** Workflow finished successfully. */
    SUCCESS,

    /** Workflow finished with an error. */
    FAILURE,

    /** Workflow was cancelled before completion. */
    CANCELLED
}