package com.axentx.surrogate1;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * A simple, thread‑safe, in‑memory conversation history tracker.
 *
 * <p>Each {@link Entry} represents a single turn – the user’s message and the assistant’s reply –
 * together with the exact instant it was recorded.  The class is intentionally lightweight
 * and does not depend on any external libraries beyond the JDK.
 */
public final class ConversationHistory {

    /**
     * Immutable record for a single conversation turn.
     */
    public static final class Entry {
        private final Instant timestamp;
        private final String userMessage;
        private final String assistantReply;

        public Entry(Instant timestamp, String userMessage, String assistantReply) {
            this.timestamp = timestamp;
            this.userMessage = userMessage;
            this.assistantReply = assistantReply;
        }

        public Instant getTimestamp() {
            return timestamp;
        }

        public String getUserMessage() {
            return userMessage;
        }

        public String getAssistantReply() {
            return assistantReply;
        }

        @Override
        public String toString() {
            return "Entry{" +
                    "timestamp=" + timestamp +
                    ", userMessage='" + userMessage + '\'' +
                    ", assistantReply='" + assistantReply + '\'' +
                    '}';
        }
    }

    // The underlying list is wrapped in a synchronizedList to guarantee thread safety.
    private final List<Entry> history = Collections.synchronizedList(new ArrayList<>());

    /**
     * Adds a new turn to the conversation history.
     *
     * @param userMessage    the message sent by the user (must not be {@code null})
     * @param assistantReply the assistant’s reply (must not be {@code null})
     * @throws IllegalArgumentException if either argument is {@code null}
     */
    public void addTurn(String userMessage, String assistantReply) {
        if (userMessage == null || assistantReply == null) {
            throw new IllegalArgumentException("Messages cannot be null");
        }
        history.add(new Entry(Instant.now(), userMessage, assistantReply));
    }

    /**
     * Returns an unmodifiable copy of the entire conversation history.
     *
     * @return a snapshot list of {@link Entry} objects
     */
    public List<Entry> getAll() {
        synchronized (history) {
            return List.copyOf(history);
        }
    }

    /**
     * Clears all recorded turns.
     */
    public void clear() {
        history.clear();
    }

    /**
     * Returns the number of turns recorded.
     *
     * @return the size of the history
     */
    public int size() {
        return history.size();
    }
}