package com.axentx.rat.controller;

import com.axentx.rat.model.BalanceHistory;
import com.axentx.rat.service.BalanceHistoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import java.util.List;

@RestController
public class HistoryController {

    @Autowired
    private BalanceHistoryService balanceHistoryService;

    @GetMapping("/api/v1/rat/history")
    public List<BalanceHistory> getHistory(
            @RequestParam(defaultValue = "0") @Min(0) int page,
            @RequestParam(defaultValue = "30") @Min(1) @Max(100) int size) {

        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "date"));
        Page<BalanceHistory> balanceHistoryPage = balanceHistoryService.findAll(pageable);

        if (balanceHistoryPage.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No balance history found");
        }

        return balanceHistoryPage.getContent();
    }
}