package com.axentx.surrogate1.model;

import java.math.BigDecimal;
import java.time.Instant;

/**
 * Minimal representation of a financial transaction.
 * Positive {@code amount} indicates revenue, negative indicates expense.
 */
public class Transaction {
    private final String id;
    private final Instant timestamp;
    private final BigDecimal amount;

    public Transaction(String id, Instant timestamp, BigDecimal amount) {
        this.id = id;
        this.timestamp = timestamp;
        this.amount = amount;
    }

    public String getId() {
        return id;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public BigDecimal getAmount() {
        return amount;
    }
}