package com.axentx.surrogate1.repository;

import com.axentx.surrogate1.model.Transaction;

import java.time.Instant;
import java.util.List;

/**
 * Simple repository abstraction for fetching transactions.
 * In production this would be backed by a database or data lake.
 */
public interface TransactionRepository {
    /**
     * Returns all transactions whose {@code timestamp} is after the supplied instant.
     *
     * @param after the lower bound (exclusive) for transaction timestamps
     * @return list of matching transactions, possibly empty but never {@code null}
     */
    List<Transaction> findByTimestampAfter(Instant after);
}