package com.axentx.surrogate1.optimization;

import com.axentx.surrogate1.model.Session;
import com.axentx.surrogate1.model.CostOptimizationActivity;

/**
 * Stateless utility that decides whether a session should be cost‑optimized
 * based on predefined usage patterns.
 *
 * The current implementation uses a very simple rule set:
 *   • If a session's average token usage per minute is below {@code LOW_USAGE_THRESHOLD},
 *     the session is marked for “resource reduction”.
 *   • If a session has been idle for longer than {@code IDLE_TIMEOUT_MS},
 *     the session is marked for “termination”.
 *
 * Real‑world logic would be driven by a configurable policy store.
 */
public final class CostOptimizer {

    private static final double LOW_USAGE_THRESHOLD = 5.0; // tokens per minute
    private static final long IDLE_TIMEOUT_MS = 10 * 60 * 1000; // 10 minutes

    private CostOptimizer() {
        // utility class – no instances
    }

    /**
     * Evaluates a session and returns an optional {@link CostOptimizationActivity}
     * describing the action taken. If no action is required, {@code null} is returned.
     */
    public static CostOptimizationActivity optimize(Session session) {
        if (session == null) {
            return null;
        }

        // Example usage‑pattern check: low token throughput
        double avgTokensPerMinute = session.getAverageTokensPerMinute();
        if (avgTokensPerMinute < LOW_USAGE_THRESHOLD) {
            // Reduce allocated resources (e.g., lower model temperature, drop caching)
            session.setResourceTier(Session.ResourceTier.LOW_COST);
            return new CostOptimizationActivity(
                    session.getId(),
                    "Reduced resources due to low usage",
                    java.time.Instant.now()
            );
        }

        // Example idle‑check
        long idleMs = java.time.Duration.between(session.getLastActivity(), java.time.Instant.now()).toMillis();
        if (idleMs > IDLE_TIMEOUT_MS) {
            session.setActive(false);
            return new CostOptimizationActivity(
                    session.getId(),
                    "Terminated idle session",
                    java.time.Instant.now()
            );
        }

        // No optimization needed
        return null;
    }
}