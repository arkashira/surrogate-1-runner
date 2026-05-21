package com.axentx.surrogate1.util;

import java.util.concurrent.Callable;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Utility for executing operations with a retry mechanism that uses exponential
 * backoff and jitter. This class is deliberately lightweight and does not depend
 * on any external libraries, making it suitable for use across all LLM provider
 * integrations.
 *
 * <p>Typical usage:
 *
 * <pre>{@code
 * String result = RetryHandler.executeWithRetry(() -> someLlmCall(prompt));
 * }</pre>
 *
 * <p>The default configuration retries up to 5 times with an initial delay of
 * 500 ms, doubling the delay after each attempt and capping it at 30 seconds.
 * Callers can supply custom {@code maxAttempts} and {@code initialDelayMs}
 * values if needed.
 */
public final class RetryHandler {

    private static final Logger LOGGER = Logger.getLogger(RetryHandler.class.getName());

    // Prevent instantiation
    private RetryHandler() {}

    /**
     * Executes the supplied operation with the default retry configuration.
     *
     * @param operation the operation to execute
     * @param <T>       the type of the operation's result
     * @return the result of the operation
     * @throws Exception if the operation fails after all retry attempts
     */
    public static <T> T executeWithRetry(Callable<T> operation) throws Exception {
        return executeWithRetry(operation, 5, 500);
    }

    /**
     * Executes the supplied operation with a configurable retry policy.
     *
     * @param operation       the operation to execute
     * @param maxAttempts     maximum number of attempts (including the first)
     * @param initialDelayMs  initial backoff delay in milliseconds
     * @param <T>             the type of the operation's result
     * @return the result of the operation
     * @throws Exception if the operation fails after all retry attempts
     */
    public static <T> T executeWithRetry(Callable<T> operation, int maxAttempts, long initialDelayMs) throws Exception {
        if (operation == null) {
            throw new IllegalArgumentException("operation must not be null");
        }
        if (maxAttempts < 1) {
            throw new IllegalArgumentException("maxAttempts must be >= 1");
        }
        if (initialDelayMs < 0) {
            throw new IllegalArgumentException("initialDelayMs must be >= 0");
        }

        long delay = initialDelayMs;
        final long maxDelay = 30_000L; // 30 seconds cap

        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return operation.call();
            } catch (Exception e) {
                if (attempt == maxAttempts) {
                    LOGGER.log(Level.SEVERE, "All retry attempts exhausted after {0} attempts", attempt);
                    throw e;
                }

                // Compute jittered backoff: delay + random(0, delay)
                long jitter = (long) (Math.random() * delay);
                long sleepTime = delay + jitter;

                LOGGER.log(Level.WARNING,
                        String.format("Attempt %d/%d failed: %s. Retrying in %d ms.", attempt, maxAttempts, e.getMessage(), sleepTime));

                try {
                    Thread.sleep(sleepTime);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw ie;
                }

                // Exponential backoff for next iteration
                delay = Math.min(delay * 2, maxDelay);
            }
        }

        // This line should never be reached
        throw new IllegalStateException("RetryHandler exhausted without returning or throwing");
    }
}