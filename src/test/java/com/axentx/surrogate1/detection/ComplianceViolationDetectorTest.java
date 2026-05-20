package com.axentx.surrogate1.detection;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ComplianceViolationDetectorTest {

    @Test
    void testDetectViolations() {
        ComplianceViolationDetector detector = new ComplianceViolationDetector();

        ComplianceViolationDetector.Resource compliantBucket =
                new ComplianceViolationDetector.Resource("bucket-1", "S3Bucket", false);
        ComplianceViolationDetector.Resource violatingBucket =
                new ComplianceViolationDetector.Resource("bucket-2", "S3Bucket", true);
        ComplianceViolationDetector.Resource otherResource =
                new ComplianceViolationDetector.Resource("vm-1", "EC2Instance", false);

        List<ComplianceViolationDetector.Resource> resources =
                Arrays.asList(compliantBucket, violatingBucket, otherResource);

        List<ComplianceViolationDetector.Violation> violations = detector.detectViolations(resources);

        assertEquals(1, violations.size(), "Should detect one violation");
        ComplianceViolationDetector.Violation violation = violations.get(0);
        assertEquals(violatingBucket, violation.getResource(), "Violation should be on the public bucket");
        assertEquals("Public S3 bucket detected", violation.getDescription());
        assertEquals("Disable public access or restrict permissions", violation.getRemediation());
    }

    @Test
    void testNoViolations() {
        ComplianceViolationDetector detector = new ComplianceViolationDetector();

        ComplianceViolationDetector.Resource resource =
                new ComplianceViolationDetector.Resource("bucket-1", "S3Bucket", false);

        List<ComplianceViolationDetector.Violation> violations =
                detector.detectViolations(Arrays.asList(resource));

        assertTrue(violations.isEmpty(), "No violations should be detected for compliant resources");
    }
}