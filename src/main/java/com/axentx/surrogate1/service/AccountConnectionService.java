package com.axentx.surrogate1.service;

import com.axentx.surrogate1.dto.AccountResponse;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class AccountConnectionService {

    private List<AccountResponse> connectedAccounts = new ArrayList<>();

    public AccountResponse connectRetirementAccount(String accountId, String provider) {
        // Implementation for connecting to external provider
        AccountResponse account = new AccountResponse(accountId, provider, "CONNECTED");
        connectedAccounts.add(account);
        return account;
    }

    public Iterable<AccountResponse> getConnectedAccounts() {
        return connectedAccounts;
    }

    public void disconnectAccount(String accountId) {
        connectedAccounts.removeIf(account -> account.getAccountId().equals(accountId));
    }
}