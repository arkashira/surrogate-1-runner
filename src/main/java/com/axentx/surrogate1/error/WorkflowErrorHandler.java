package com.axentx.surrogate1.error;

import java.util.logging.Logger;
import java.util.ResourceBundle;

public class WorkflowErrorHandler {
    private static final Logger logger = Logger.getLogger(WorkflowErrorHandler.class.getName());
    private static final ResourceBundle errorMessages = ResourceBundle.getBundle("error-messages");

    public void handleWorkflowError(Exception e) {
        String errorMessage = String.format(errorMessages.getString("workflow.error.message"), e.getMessage());
        logger.severe(errorMessage);
        logErrorDetails(e);
        logErrorMetrics("workflow", e);
    }

    public void handleFileGenerationError(Exception e) {
        String errorMessage = String.format(errorMessages.getString("file.generation.error.message"), e.getMessage());
        logger.severe(errorMessage);
        logErrorDetails(e);
        logErrorMetrics("file generation", e);
    }

    private void logErrorDetails(Exception e) {
        logger.info(String.format(errorMessages.getString("error.details"), e.getStackTrace()));
    }

    private void logErrorMetrics(String processType, Exception e) {
        // Assuming a method to extract metrics (e.g., execution time, error type, error frequency) from the exception or process type
        String errorMetrics = extractErrorMetrics(processType, e);
        logger.info(String.format(errorMessages.getString("error.metrics"), errorMetrics));
    }

    // Example method to extract error metrics; actual implementation depends on the specific requirements
    private String extractErrorMetrics(String processType, Exception e) {
        // Logic to extract or calculate error metrics based on processType and exception details
        return "example metrics: " + processType + " time, error type, and error frequency";
    }
}