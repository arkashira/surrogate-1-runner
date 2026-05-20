package com.axentx.surrogate.workflow;

import java.util.List;

public class WorkflowConfig {
    private String workflowName;
    private String description;
    private List<String> steps;
    private String triggerCondition;
    private int threadCount;
    private String storagePath;
    private long timeoutSeconds;

    public WorkflowConfig(String workflowName, String description, List<String> steps, String triggerCondition, int threadCount, String storagePath, long timeoutSeconds) {
        this.workflowName = workflowName;
        this.description = description;
        this.steps = steps;
        this.triggerCondition = triggerCondition;
        this.threadCount = threadCount;
        this.storagePath = storagePath;
        this.timeoutSeconds = timeoutSeconds;
    }

    public String getWorkflowName() {
        return workflowName;
    }

    public void setWorkflowName(String workflowName) {
        this.workflowName = workflowName;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<String> getSteps() {
        return steps;
    }

    public void setSteps(List<String> steps) {
        this.steps = steps;
    }

    public String getTriggerCondition() {
        return triggerCondition;
    }

    public void setTriggerCondition(String triggerCondition) {
        this.triggerCondition = triggerCondition;
    }

    public int getThreadCount() {
        return threadCount;
    }

    public void setThreadCount(int threadCount) {
        this.threadCount = threadCount;
    }

    public String getStoragePath() {
        return storagePath;
    }

    public void setStoragePath(String storagePath) {
        this.storagePath = storagePath;
    }

    public long getTimeoutSeconds() {
        return timeoutSeconds;
    }

    public void setTimeoutSeconds(long timeoutSeconds) {
        this.timeoutSeconds = timeoutSeconds;
    }
}