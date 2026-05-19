package com.axentx.surrogate1.orchestration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class StatusReporter {

    @Autowired
    private WorkflowStatus workflowStatus;

    @Scheduled(fixedRate = 5000) // Report status every 5 seconds
    public void reportStatus() {
        if (workflowStatus.isPaused()) {
            System.out.println("Workflow is paused. Reason: " + workflowStatus.getPauseReason());
            System.out.println("Metadata: " + workflowStatus.getPauseMetadata());
        } else {
            System.out.println("Workflow is running. Current step: " + workflowStatus.getCurrentStep());
        }
    }
}