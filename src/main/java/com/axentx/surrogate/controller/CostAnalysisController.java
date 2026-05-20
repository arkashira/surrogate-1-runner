package com.axentx.surrogate.controller;

import com.axentx.surrogate.model.CostAnalysis;
import com.axentx.surrogate.model.CostIncrease;
import com.axentx.surrogate.service.CostAnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cost-analysis")
public class CostAnalysisController {

    @Autowired
    private CostAnalysisService costAnalysisService;

    @GetMapping("/cost-increases")
    public List<CostIncrease> getCostIncreases() {
        return costAnalysisService.getCostIncreases();
    }

    @GetMapping("/root-cause/{costIncreaseId}")
    public CostAnalysis getRootCauseAnalysis(@PathVariable Long costIncreaseId) {
        return costAnalysisService.getRootCauseAnalysis(costIncreaseId);
    }

    @PostMapping("/save")
    public void saveCostAnalysis(@RequestBody CostAnalysis costAnalysis) {
        costAnalysisService.saveCostAnalysis(costAnalysis);
    }
}