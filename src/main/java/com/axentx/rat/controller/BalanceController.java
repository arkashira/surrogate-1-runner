package com.axentx.rat.controller;

import com.axentx.rat.dto.BalanceResponse;
import com.axentx.rat.service.BalanceService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/rat")
public class BalanceController {

    private final BalanceService balanceService;

    public BalanceController(BalanceService balanceService) {
        this.balanceService = balanceService;
    }

    @GetMapping("/balance")
    public ResponseEntity<BalanceResponse> getConsolidatedBalance() {
        BalanceResponse response = balanceService.getConsolidatedBalance();
        return ResponseEntity.ok(response);
    }
}