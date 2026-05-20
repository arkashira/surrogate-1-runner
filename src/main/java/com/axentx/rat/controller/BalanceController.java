package com.axentx.rat.controller;

import io.micrometer.core.annotation.Timed;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/balance")
public class BalanceController {

    private final Counter apiRequestsCounter;
    private final MeterRegistry meterRegistry;

    public BalanceController(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.apiRequestsCounter = Counter.builder("rat_api_requests_total")
                .tag("endpoint", "balance")
                .register(meterRegistry);
    }

    @GetMapping
    @Timed(value = "rat_api_latency_seconds", extraTags = {"endpoint", "balance"})
    public String getBalance() {
        apiRequestsCounter.increment();
        // Existing balance logic here
        return "balance";
    }
}