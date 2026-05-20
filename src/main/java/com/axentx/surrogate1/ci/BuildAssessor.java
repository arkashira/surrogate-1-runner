package com.axentx.surrogate1.ci;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.sonarqube.ws.Client;
import org.sonarqube.ws.Report;

public class BuildAssessor {
    private static final Logger LOG = LoggerFactory.getLogger(BuildAssessor.class);

    public void assess(Client client, String projectKey) {
        try {
            Report report = client.getReport(projectKey);
            LOG.info("Vulnerability assessment completed for project: {}", projectKey);
            LOG.info("Total vulnerabilities: {}", report.getVulnerabilities().getTotal());
        } catch (Exception e) {
            LOG.error("Error performing vulnerability assessment: ", e);
        }
    }
}