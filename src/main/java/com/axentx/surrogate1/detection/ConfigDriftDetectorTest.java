package com.axentx.surrogate1.detection;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ConfigDriftDetectorTest {

    @Test
    public void testDetectDrift() {
        ConfigDriftDetector detector = new ConfigDriftDetector();
        detector.setBaselineConfiguration("resource1", "config1");

        assertFalse(detector.detectDrift("resource1", "config1"));
        assertTrue(detector.detectDrift("resource1", "config2"));
    }

    @Test
    public void testGetRemediationSuggestion() {
        ConfigDriftDetector detector = new ConfigDriftDetector();
        detector.setBaselineConfiguration("resource1", "config1");

        assertEquals("Revert configuration to: config1", detector.getRemediationSuggestion("resource1", "config2"));
        assertEquals("No baseline configuration found for resource.", detector.getRemediationSuggestion("resource2", "config3"));
    }
}