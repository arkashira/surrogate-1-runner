package com.axentx.surrogate1.cost;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * Exposes cost data via HTTP.
 */
@RestController
@RequestMapping("/api/cost")
public class CostBreakdownController {

    @Autowired
    private CostBreakdownService costBreakdownService;

    @GetMapping("/breakdown")
    public Map<String, Double> getCostBreakdown() {
        return costBreakdownService.getCostBreakdownByResourceType();
    }

    @GetMapping("/total")
    public double getTotalCost() {
        return costBreakdownService.getTotalCost();
    }
}