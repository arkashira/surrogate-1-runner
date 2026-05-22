package com.axentx.surrogate1.collaboration.domain;

import java.time.Instant;
import java.util.Objects;

public final class CostInsight {
    private final String id;
    private final String title;
    private final String description;
    private final double amount;
    private final String currency;
    private final String category;
    private final String sharedBy;
    private final Instant createdAt;

    public CostInsight(String id, String title, String description,
                       double amount, String currency, String category,
                       String sharedBy, Instant createdAt) {
        this.id = Objects.requireNonNull(id);
        this.title = Objects.requireNonNull(title);
        this.description = Objects.requireNonNull(description);
        this.amount = amount;
        this.currency = Objects.requireNonNull(currency);
        this.category = Objects.requireNonNull(category);
        this.sharedBy = Objects.requireNonNull(sharedBy);
        this.createdAt = Objects.requireNonNull(createdAt);
    }

    // getters …
}