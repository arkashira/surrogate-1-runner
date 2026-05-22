package com.axentx.surrogate1.api;

import com.axentx.surrogate1.dto.ConnectAccountRequest;
import com.axentx.surrogate1.dto.AccountResponse;
import com.axentx.surrogate1.service.AccountConnectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/accounts")
public class AccountConnectionController {

    @Autowired
    private AccountConnectionService accountService;

    @PostMapping("/connect")
    public AccountResponse connectAccount(@RequestBody ConnectAccountRequest request) {
        return accountService.connectRetirementAccount(request.getAccountId(), request.getProvider());
    }

    @GetMapping
    public Iterable<AccountResponse> getConnectedAccounts() {
        return accountService.getConnectedAccounts();
    }

    @DeleteMapping("/{accountId}")
    public void disconnectAccount(@PathVariable String accountId) {
        accountService.disconnectAccount(accountId);
    }
}