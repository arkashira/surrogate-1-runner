package com.axentx.surrogate1;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Consumer;

/**
 * Manages playback quality feedback collection and delivery.
 * Allows users to receive feedback and adjust settings accordingly.
 */
public class FeedbackManager {
    
    private final Map<String, List<PlaybackQualityFeedback>> sessionFeedback;
    private final Database database;
    
    public FeedbackManager(Database database) {
        this.sessionFeedback = new ConcurrentHashMap<>();
        this.database = database;
    }
    
    /**
     * Collects playback quality feedback for a given session.
     * 
     * @param sessionId the ID of the session
     * @param feedback the playback quality feedback
     */
    public void collectFeedback(String sessionId, PlaybackQualityFeedback feedback) {
        sessionFeedback.computeIfAbsent(sessionId, k -> new ArrayList<>()).add(feedback);
        database.storeFeedback(sessionId, feedback);
    }
    
    /**
     * Delivers playback quality feedback to a user.
     * 
     * @param sessionId the ID of the session
     * @param consumer a consumer that handles the feedback
     */
    public void deliverFeedback(String sessionId, Consumer<PlaybackQualityFeedback> consumer) {
        List<PlaybackQualityFeedback> feedback = sessionFeedback.get(sessionId);
        if (feedback != null) {
            feedback.forEach(consumer);
        } else {
            database.retrieveFeedback(sessionId).ifPresent(consumer);
        }
    }
    
    /**
     * Retrieves playback quality feedback for a given session.
     * 
     * @param sessionId the ID of the session
     * @return the playback quality feedback
     */
    public List<PlaybackQualityFeedback> retrieveFeedback(String sessionId) {
        return sessionFeedback.get(sessionId);
    }
    
    /**
     * Stores playback quality feedback in the database.
     * 
     * @param sessionId the ID of the session
     * @param feedback the playback quality feedback
     */
    private void storeFeedback(String sessionId, PlaybackQualityFeedback feedback) {
        database.storeFeedback(sessionId, feedback);
    }
    
    /**
     * Retrieves playback quality feedback from the database.
     * 
     * @param sessionId the ID of the session
     * @return the playback quality feedback
     */
    private Optional<PlaybackQualityFeedback> retrieveFeedbackFromDatabase(String sessionId) {
        return database.retrieveFeedback(sessionId);
    }
}

interface Database {
    void storeFeedback(String sessionId, PlaybackQualityFeedback feedback);
    Optional<PlaybackQualityFeedback> retrieveFeedback(String sessionId);
}