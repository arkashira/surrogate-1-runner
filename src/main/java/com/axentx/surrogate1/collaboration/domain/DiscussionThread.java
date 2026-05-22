package com.axentx.surrogate1.collaboration.domain;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public final class DiscussionThread {
    private final String id;
    private final String insightId;
    private final String title;
    private final Instant createdAt;
    private final List<DiscussionMessage> messages = new ArrayList<>();

    public DiscussionThread(String id, String insightId, String title, Instant createdAt) {
        this.id = Objects.requireNonNull(id);
        this.insightId = Objects.requireNonNull(insightId);
        this.title = Objects.requireNonNull(title);
        this.createdAt = Objects.requireNonNull(createdAt);
    }

    public synchronized void addMessage(DiscussionMessage msg) {
        messages.add(msg);
    }

    public List<DiscussionMessage> getMessages() {
        return Collections.unmodifiableList(messages);
    }

    // getters …
}