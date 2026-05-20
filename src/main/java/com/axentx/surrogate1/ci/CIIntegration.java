package com.axentx.surrogate1.ci;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.sonarqube.ws.Client;

public class CIIntegration {
    private static final Logger LOG = LoggerFactory.getLogger(CIIntegration.class);
    private final Client sonarqubeClient;

    public CIIntegration(Client sonarqubeClient) {
        this.sonarqubeClient = sonarqubeClient;
    }

    public void integrateBuildAssessment(String projectKey) {
        BuildAssessor assessor = new BuildAssessor();
        assessor.assess(sonarqubeClient, projectKey);
    }
}