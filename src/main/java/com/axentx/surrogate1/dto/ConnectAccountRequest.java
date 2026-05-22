package com.axentx.surrogate1.dto;

public class ConnectAccountRequest {
    private String accountId;
    private String provider;

    // Getters and setters
    public String getAccountId() { return accountId; }
    public void setAccountId(String accountId) { this.accountId = accountId; }

    public String getProvider() { return provider; }
    public void setProvider(String provider) { this.provider = provider; }
}