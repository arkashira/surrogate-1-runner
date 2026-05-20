package com.axentx.surrogate1.model;

import java.time.Instant;

/**
 * Represents a single cost‑optimization action performed on a session.
 */
public class CostOptimizationActivity {

    private final String sessionId;
    private final String action;
    private final Instant timestamp;

    public CostOptimizationActivity(String sessionId, String action, Instant timestamp) {
        this.sessionId = sessionId;
        this.action = action;
        this.timestamp = timestamp;
    }

    public String getSessionId() {
        return sessionId;
    }

    public String getAction() {
        return action;
    }

    public Instant getTimestamp() {
        return timestamp;
    }
}