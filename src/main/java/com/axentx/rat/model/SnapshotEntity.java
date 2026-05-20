package com.axentx.rat.model;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;

@Entity
@Table(name = "snapshot")
public class SnapshotEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Provider name (e.g., "ProviderA")
    @Column(nullable = false)
    private String provider;

    // Date of the snapshot (e.g., 2023-09-01)
    @Column(name = "snapshot_date", nullable = false)
    private LocalDate snapshotDate;

    // Balance in USD for this provider on the snapshot date
    @Column(name = "balance_usd", nullable = false, precision = 19, scale = 4)
    private BigDecimal balanceUsd;

    // Timestamp when this row was last updated
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected SnapshotEntity() {
        // JPA requirement
    }

    public SnapshotEntity(String provider, LocalDate snapshotDate, BigDecimal balanceUsd, Instant updatedAt) {
        this.provider = provider;
        this.snapshotDate = snapshotDate;
        this.balanceUsd = balanceUsd;
        this.updatedAt = updatedAt;
    }

    public Long getId() {
        return id;
    }

    public String getProvider() {
        return provider;
    }

    public LocalDate getSnapshotDate() {
        return snapshotDate;
    }

    public BigDecimal getBalanceUsd() {
        return balanceUsd;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }
}