package com.axentx.surrogate1.dto;

public class AccountResponse {
    private String accountId;
    private String provider;
    private String status;

    // Constructor, getters and setters
    public AccountResponse(String accountId, String provider, String status) {
        this.accountId = accountId;
        this.provider = provider;
        this.status = status;
    }

    public String getAccountId() { return accountId; }
    public String getProvider() { return provider; }
    public String getStatus() { return status; }
}