package com.axentx.surrogate1.notification;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.function.Consumer;

/**
 * Service responsible for notifying about API signature drift.
 */
public class NotificationService {
    private final List<AlertChannel> alertChannels;

    /**
     * Creates a new NotificationService.
     * @param alertChannels The list of channels used to send alerts
     */
    public NotificationService(List<AlertChannel> alertChannels) {
        this.alertChannels = alertChannels;
    }

    /**
     * Sends a notification that a signature drift has been detected.
     * @param signature The API request signature that drifted
     * @param notifyOnSuccess Whether to notify on success (e.g., for testing)
     */
    public void notifySignatureDrift(String signature, boolean notifyOnSuccess) {
        String message = String.format("Signature drift detected: %s", signature);
        CompletableFuture<Void> future = CompletableFuture.allOf();

        for (AlertChannel channel : alertChannels) {
            if (channel.isEnabled()) {
                CompletableFuture<Boolean> sendFuture = channel.send("Signature Drift Alert", message, Map.of("signature", signature));
                future = future.thenCombine(sendFuture, (v, b) -> v);
            }
        }

        if (notifyOnSuccess && future.isCompletedExceptionally()) {
            throw new RuntimeException("Failed to send notifications");
        }
    }
}