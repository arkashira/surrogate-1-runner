package com.axentx.surrogate1;

import com.amazonaws.services.securityhub.AWSecurityHub;
import com.amazonaws.services.securityhub.AWSecurityHubClient;
import com.amazonaws.services.securityhub.model.FindSecurityHubStandardsControlAssessmentsRequest;
import com.amazonaws.services.securityhub.model.FindSecurityHubStandardsControlAssessmentsResult;
import com.amazonaws.services.securityhub.model.SecurityHubStandardsControlAssessment;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.securityhub.SecurityHubClient;
import software.amazon.awssdk.services.securityhub.model.FindSecurityHubStandardsControlAssessmentsRequest;
import software.amazon.awssdk.services.securityhub.model.FindSecurityHubStandardsControlAssessmentsResponse;
import software.amazon.awssdk.services.securityhub.model.SecurityHubStandardsControlAssessment;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class AwsApi {

    private final SecurityHubClient securityHubClient;

    public AwsApi() {
        this.securityHubClient = SecurityHubClient.builder()
                .region(Region.US_EAST_1)
                .build();
    }

    public List<SecurityHubStandardsControlAssessment> getSecurityHubAssessments() {
        FindSecurityHubStandardsControlAssessmentsRequest request = FindSecurityHubStandardsControlAssessmentsRequest.builder()
                .build();

        FindSecurityHubStandardsControlAssessmentsResponse response = securityHubClient.findSecurityHubStandardsControlAssessments(request);

        return response.assessments().stream()
                .collect(Collectors.toList());
    }
}