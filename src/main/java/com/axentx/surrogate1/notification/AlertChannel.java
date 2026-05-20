package com.axentx.surrogate1.notification;

import java.util.Map;
import java.util.Properties;
import javax.mail.*;
import javax.mail.internet.*;

/**
 * Interface for alert channels (email, Slack, etc.)
 */
public interface AlertChannel {
    /**
     * Send an alert notification
     * @param title The alert title
     * @param message The alert message body
     * @param metadata Additional metadata (e.g., signature details, timestamps)
     * @return CompletableFuture<Boolean> representing the result of the send operation
     */
    CompletableFuture<Boolean> send(String title, String message, Map<String, String> metadata);

    /**
     * @return The channel name (e.g., "email", "slack")
     */
    String getChannelName();

    /**
     * Check if this channel is enabled/configured
     * @return true if the channel can send notifications
     */
    boolean isEnabled();
}