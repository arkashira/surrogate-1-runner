package com.axentx.surrogate1.collaboration.domain;

import java.time.Instant;
import java.util.Objects;

public final class DiscussionMessage {
    private final String id;
    private final String threadId;
    private final String author;
    private final String content;
    private final Instant createdAt;

    public DiscussionMessage(String id, String threadId, String author,
                             String content, Instant createdAt) {
        this.id = Objects.requireNonNull(id);
        this.threadId = Objects.requireNonNull(threadId);
        this.author = Objects.requireNonNull(author);
        this.content = Objects.requireNonNull(content);
        this.createdAt = Objects.requireNonNull(createdAt);
    }

    // getters …
}