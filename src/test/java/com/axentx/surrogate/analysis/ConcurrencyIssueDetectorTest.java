package com.axentx.surrogate.analysis;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class ConcurrencyIssueDetectorTest {

    @Test
    public void testDetectConcurrencyIssues() {
        ConcurrencyIssueDetector detector = new ConcurrencyIssueDetector();
        List<String> codeFiles = Arrays.asList(
                "codeFile1",
                "codeFile2"
        );

        List<String> issues = detector.detectConcurrencyIssues("sampleCode");
        assertTrue(issues.size() >= 1, "Should detect at least one concurrency issue");

        detector.analyzeCodeBase(codeFiles);
    }
}