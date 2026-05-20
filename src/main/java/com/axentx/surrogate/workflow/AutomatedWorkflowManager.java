package com.axentx.surrogate.workflow;

import java.time.Instant;
import java.util.Collections;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * A lightweight in-memory manager for automated design workflows.
 *
 * <p>Workflows are represented by a unique UUID and can be created, started, completed,
 * cancelled, and queried. The manager uses a single-threaded {@link ExecutorService}
 * to execute workflow tasks serially, which keeps the implementation simple and
 * deterministic for unit testing. In a production environment this could be
 * swapped out for a more robust scheduler.</p>
 */
public class AutomatedWorkflowManager {

    /** Internal representation of a workflow. */
    private static class Workflow {
        final String id;
        final String name;
        volatile WorkflowStatus status;
        volatile Instant startedAt;
        volatile Instant finishedAt;
        volatile String errorMessage;

        Workflow(String name) {
            this.id = UUID.randomUUID().toString();
            this.name = name;
            this.status = WorkflowStatus.PENDING;
        }
    }

    private final Map<String, Workflow> workflows = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    /**
     * Creates a new workflow with the given name.
     *
     * @param name human‑readable workflow name
     * @return the generated workflow ID
     */
    public String createWorkflow(String name) {
        Workflow wf = new Workflow(name);
        workflows.put(wf.id, wf);
        return wf.id;
    }

    /**
     * Starts the workflow identified by {@code workflowId}.
     *
     * @param workflowId the ID returned by {@link #createWorkflow}
     * @param task the actual work to perform; should be a {@link Runnable}
     * @return a {@link Future} that completes when the task finishes
     * @throws IllegalStateException if the workflow is not in {@link WorkflowStatus#PENDING}
     */
    public Future<?> startWorkflow(String workflowId, Runnable task) {
        Workflow wf = workflows.get(workflowId);
        if (wf == null) {
            throw new IllegalArgumentException("Unknown workflow ID: " + workflowId);
        }
        if (wf.status != WorkflowStatus.PENDING) {
            throw new IllegalStateException(
                "Cannot start workflow in state: " + wf.status);
        }
        wf.status = WorkflowStatus.RUNNING;
        wf.startedAt = Instant.now();

        return executor.submit(() -> {
            try {
                task.run();
                wf.status = WorkflowStatus.SUCCESS;
            } catch (Throwable t) {
                wf.status = WorkflowStatus.FAILURE;
                wf.errorMessage = t.getMessage();
                throw t;
            } finally {
                wf.finishedAt = Instant.now();
            }
        });
    }

    /**
     * Cancels a running workflow. If the workflow is already finished, this is a no‑op.
     *
     * @param workflowId the ID of the workflow to cancel
     * @return {@code true} if the workflow was cancelled, {@code false} otherwise
     */
    public boolean cancelWorkflow(String workflowId) {
        Workflow wf = workflows.get(workflowId);
        if (wf == null) {
            return false;
        }
        if (wf.status == WorkflowStatus.RUNNING) {
            // In a real implementation we would interrupt the running task.
            // Here we simply mark it as cancelled; the executor will finish the current task.
            wf.status = WorkflowStatus.CANCELLED;
            wf.finishedAt = Instant.now();
            return true;
        }
        return false;
    }

    /**
     * Retrieves the current status of a workflow.
     *
     * @param workflowId the workflow ID
     * @return the {@link WorkflowStatus}
     * @throws IllegalArgumentException if the ID is unknown
     */
    public WorkflowStatus getStatus(String workflowId) {
        Workflow wf = workflows.get(workflowId);
        if (wf == null) {
            throw new IllegalArgumentException("Unknown workflow ID: " + workflowId);
        }
        return wf.status;
    }

    /**
     * Returns an unmodifiable view of all workflow IDs.
     *
     * @return set of workflow IDs
     */
    public Map<String, WorkflowStatus> listWorkflows() {
        return Collections.unmodifiableMap(
            workflows.entrySet().stream()
                .collect(
                    java.util.stream.Collectors.toMap(
                        Map.Entry::getKey,
                        e -> e.getValue().status)));
    }

    /**
     * Gracefully shuts down the internal executor. Should be called during application
     * shutdown to avoid resource leaks.
     */
    public void shutdown() {
        executor.shutdownNow();
    }
}