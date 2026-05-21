package com.axentx.surrogate.pipeline;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.axentx.surrogate.notification.EmailNotificationService;

@Service
public class PipelineService {

    private final EmailNotificationService emailNotificationService;

    @Autowired
    public PipelineService(EmailNotificationService emailNotificationService) {
        this.emailNotificationService = emailNotificationService;
    }

    /**
     * Called when a pipeline finishes execution.
     *
     * @param pipelineName the unique name/identifier of the pipeline
     * @param success      true if the pipeline succeeded, false if it failed
     * @param dashboardUrl URL to the dashboard view for this pipeline run
     */
    public void handlePipelineCompletion(String pipelineName, boolean success, String dashboardUrl) {
        // Existing business logic ... (omitted for brevity)

        // Wire email notification
        String status = success ? "COMPLETED" : "FAILED";
        emailNotificationService.notify(pipelineName, status, dashboardUrl);
    }

    // Other existing methods ...
}