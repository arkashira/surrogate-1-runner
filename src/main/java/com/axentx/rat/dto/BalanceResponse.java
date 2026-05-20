package com.axentx.rat.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;
import java.time.Instant;

public class BalanceResponse {

    @JsonProperty("total_balance_usd")
    private final BigDecimal totalBalanceUsd;

    @JsonProperty("last_updated")
    private final Instant lastUpdated;

    public BalanceResponse(BigDecimal totalBalanceUsd, Instant lastUpdated) {
        this.totalBalanceUsd = totalBalanceUsd;
        this.lastUpdated = lastUpdated;
    }

    public BigDecimal getTotalBalanceUsd() {
        return totalBalanceUsd;
    }

    public Instant getLastUpdated() {
        return lastUpdated;
    }
}