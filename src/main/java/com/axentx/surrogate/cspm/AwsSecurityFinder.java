package com.axentx.surrogate.cspm;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.securityhub.SecurityHubClient;
import software.amazon.awssdk.services.securityhub.model.*;
import java.util.*;
import java.util.stream.Collectors;

/**
 * AwsSecurityFinder is a lightweight, dependency-free component that retrieves
 * security findings from AWS Security Hub and converts them into a standardized
 * format for downstream processing.
 *
 * Key features:
 * - Multiple constructor options for different authentication scenarios
 * - Paginated fetching of all available findings
 * - Comprehensive field mapping with type safety
 * - Resource cleanup mechanism
 */
public class AwsSecurityFinder implements AutoCloseable {
    private final SecurityHubClient securityHubClient;

    /**
     * Creates a finder using default AWS credential chain and region.
     */
    public AwsSecurityFinder() {
        this(Region.of(System.getenv().getOrDefault("AWS_REGION", "us-east-1")));
    }

    /**
     * Creates a finder for a specific AWS region using default credentials.
     * @param region AWS region to target
     */
    public AwsSecurityFinder(Region region) {
        this(SecurityHubClient.builder()
            .region(region)
            .credentialsProvider(DefaultCredentialsProvider.create())
            .build());
    }

    /**
     * Creates a finder with explicit credentials and region.
     * @param accessKey AWS access key
     * @param secretKey AWS secret key
     * @param region AWS region
     */
    public AwsSecurityFinder(String accessKey, String secretKey, String region) {
        this(SecurityHubClient.builder()
            .region(Region.of(region))
            .credentialsProvider(() -> AwsBasicCredentials.create(accessKey, secretKey))
            .build());
    }

    /**
     * Creates a finder with a pre-configured SecurityHub client.
     * @param client pre-configured SecurityHub client
     */
    public AwsSecurityFinder(SecurityHubClient client) {
        this.securityHubClient = Objects.requireNonNull(client, "SecurityHubClient cannot be null");
    }

    /**
     * Retrieves all security findings from AWS Security Hub.
     * @return List of findings in standardized map format
     */
    public List<Map<String, Object>> fetchFindings() {
        try {
            return securityHubClient.getFindingsPaginator(GetFindingsRequest.builder()
                .maxResults(100)
                .build())
                .stream()
                .flatMap(response -> response.findings().stream())
                .map(this::convertFindingToMap)
                .collect(Collectors.toList());
        } catch (SecurityHubException e) {
            throw new RuntimeException("Failed to fetch AWS Security Hub findings: " + e.getMessage(), e);
        }
    }

    private Map<String, Object> convertFindingToMap(Finding finding) {
        Map<String, Object> map = new LinkedHashMap<>();

        // Core identification fields
        map.put("Id", finding.id());
        map.put("ProductArn", finding.productArn());
        map.put("GeneratorId", finding.generatorId());
        map.put("Types", finding.types());

        // Temporal information
        map.put("FirstObservedAt", finding.firstObservedAt());
        map.put("LastObservedAt", finding.lastObservedAt());
        map.put("CreatedAt", finding.createdAt());
        map.put("UpdatedAt", finding.updatedAt());

        // Severity information
        if (finding.severity() != null) {
            map.put("SeverityLabel", finding.severity().labelAsString());
            map.put("SeverityScore", finding.severity().normalized());
        }

        // Resource information
        if (finding.resources() != null && !finding.resources().isEmpty()) {
            Resource resource = finding.resources().get(0);
            map.put("ResourceId", resource.id());
            map.put("ResourceType", resource.type());
            map.put("ResourcePartition", resource.partition());
            map.put("ResourceRegion", resource.region());
        }

        // Contextual information
        map.put("Title", finding.title());
        map.put("Description", finding.description());

        // Compliance information
        if (finding.compliance() != null) {
            map.put("ComplianceStatus", finding.compliance().statusAsString());
            map.put("ComplianceRelatedRequirements", finding.compliance().relatedRequirements());
        }

        return map;
    }

    @Override
    public void close() {
        if (securityHubClient != null) {
            securityHubClient.close();
        }
    }
}