package com.axentx.surrogate1.detection;

import java.util.ArrayList;
import java.util.List;

/**
 * A simple compliance violation detector for cloud resources.
 *
 * <p>Current rule set:
 * <ul>
 *   <li>S3 buckets with public access enabled are considered non-compliant.</li>
 * </ul>
 *
 * <p>Each violation includes a remediation suggestion.
 */
public class ComplianceViolationDetector {

    /**
     * Detects compliance violations in the provided list of resources.
     *
     * @param resources the list of cloud resources to evaluate
     * @return a list of {@link Violation} objects representing each detected violation
     */
    public List<Violation> detectViolations(List<Resource> resources) {
        List<Violation> violations = new ArrayList<>();
        for (Resource resource : resources) {
            if (isPublicS3Bucket(resource)) {
                violations.add(new Violation(
                        resource,
                        "Public S3 bucket detected",
                        "Disable public access or restrict permissions"
                ));
            }
            // Future rules can be added here
        }
        return violations;
    }

    private boolean isPublicS3Bucket(Resource resource) {
        return "S3Bucket".equalsIgnoreCase(resource.getType()) && resource.isPublicAccess();
    }

    /**
     * Represents a cloud resource.
     */
    public static class Resource {
        private final String id;
        private final String type;
        private final boolean publicAccess;

        public Resource(String id, String type, boolean publicAccess) {
            this.id = id;
            this.type = type;
            this.publicAccess = publicAccess;
        }

        public String getId() {
            return id;
        }

        public String getType() {
            return type;
        }

        public boolean isPublicAccess() {
            return publicAccess;
        }
    }

    /**
     * Represents a compliance violation.
     */
    public static class Violation {
        private final Resource resource;
        private final String description;
        private final String remediation;

        public Violation(Resource resource, String description, String remediation) {
            this.resource = resource;
            this.description = description;
            this.remediation = remediation;
        }

        public Resource getResource() {
            return resource;
        }

        public String getDescription() {
            return description;
        }

        public String getRemediation() {
            return remediation;
        }
    }
}