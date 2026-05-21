package com.axentx.surrogate1.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class RiskDetectionService {

    private final RestTemplate restTemplate;
    private final String alertEndpoint;

    @Autowired
    public RiskDetectionService(RestTemplate restTemplate, String alertEndpoint) {
        this.restTemplate = restTemplate;
        this.alertEndpoint = alertEndpoint;
    }

    public void detectAndAlertRisks(String modelId, String riskType, String severity) {
        String alertMessage = createAlertMessage(modelId, riskType, severity);
        sendAlert(alertMessage);
    }

    private String createAlertMessage(String modelId, String riskType, String severity) {
        return String.format("Risk detected in model %s: %s (Severity: %s). Recommended action: Review model configuration and training data.",
                modelId, riskType, severity);
    }

    private void sendAlert(String alertMessage) {
        restTemplate.postForObject(alertEndpoint, alertMessage, String.class);
    }
}