package com.axentx.surrogate1;

import java.time.Duration;
import java.util.List;

/**
 * All tunables are immutable and must be supplied at construction time.
 */
public record DriftDetectorConfig(
        Duration periodicCheckInterval,      // e.g. PT30S
        Duration notificationTimeout,        // e.g. PT1M
        List<String> alertRecipients,        // e.g. ["sre-oncall@axentx.com"]
        String alertSubjectPrefix            // e.g. "URGENT:"
) {
    public static DriftDetectorConfig defaults() {
        return new DriftDetectorConfig(
                Duration.ofSeconds(30),
                Duration.ofSeconds(60),
                List.of("sre-oncall@axentx.com"),
                "URGENT:");
    }
}