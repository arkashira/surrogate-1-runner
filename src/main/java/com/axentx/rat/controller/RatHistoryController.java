package com.axentx.rat.controller;

import com.axentx.rat.model.HistoricalBalance;
import com.axentx.rat.service.RatHistoryService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Api(tags = "RAT History")
@RequestMapping("/api/v1/rat")
public class RatHistoryController {

    @Autowired
    private RatHistoryService ratHistoryService;

    @GetMapping("/history")
    @ApiOperation(value = "Get paginated historical balance snapshots", notes = "Returns balance, date, and account_id fields ordered by date descending")
    public ResponseEntity<Page<HistoricalBalance>> getHistoricalBalances(
            @ApiParam(value = "Page number (default: 0)", example = "0")
            @RequestParam(defaultValue = "0") int page,
            @ApiParam(value = "Page size (default: 30, max: 100)", example = "30")
            @RequestParam(defaultValue = "30") int size) {
        Page<HistoricalBalance> balances = ratHistoryService.getHistoricalBalances(page, size);
        return ResponseEntity.ok(balances);
    }
}