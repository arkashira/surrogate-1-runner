package com.axentx.rat.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class HistoricalBalance {
    private BigDecimal balance;
    private LocalDateTime date;
    private String accountId;

    // Constructors
    public HistoricalBalance() {}

    public HistoricalBalance(BigDecimal balance, LocalDateTime date, String accountId) {
        this.balance = balance;
        this.date = date;
        this.accountId = accountId;
    }

    // Getters and setters
    public BigDecimal getBalance() {
        return balance;
    }

    public void setBalance(BigDecimal balance) {
        this.balance = balance;
    }

    public LocalDateTime getDate() {
        return date;
    }

    public void setDate(LocalDateTime date) {
        this.date = date;
    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }
}