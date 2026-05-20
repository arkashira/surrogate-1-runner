package com.axentx.surrogate1;

import software.amazon.awssdk.services.securityhub.SecurityHubClient;
import software.amazon.awssdk.services.securityhub.model.FindSecurityHubStandardsControlAssessmentControlsRequest;
import software.amazon.awssdk.services.securityhub.model.FindSecurityHubStandardsControlAssessmentControlsResponse;

import java.util.List;

public class CloudProvider {
    private final SecurityHubClient securityHubClient;

    public CloudProvider(SecurityHubClient securityHubClient) {
        this.securityHubClient = securityHubClient;
    }

    public List<FindSecurityHubStandardsControlAssessmentControlsResponse> getStandardsControlAssessments() {
        FindSecurityHubStandardsControlAssessmentControlsRequest request = FindSecurityHubStandardsControlAssessmentControlsRequest.builder()
                .standardsControlAssessmentControlIds(List.of("ABC123", "DEF456")) // replace with actual control IDs
                .build();

        return securityHubClient.findSecurityHubStandardsControlAssessmentControlsPaginator(request).collectList().join();
    }
}