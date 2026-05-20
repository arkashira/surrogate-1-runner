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

    @GetMapping
    public List<CostAnalysis> getCostAnalysis() {
        return costAnalysisService.getCostAnalysis();
    }

    @PostMapping
    public CostAnalysis saveCostAnalysis(@RequestBody CostAnalysis costAnalysis) {
        return costAnalysisService.saveCostAnalysis(costAnalysis);
    }

    @GetMapping("/increases")
    public List<CostIncrease> getCostIncreases() {
        return costAnalysisService.getCostIncreases();
    }

    @GetMapping("/recommendations")
    public List<String> getRecommendations(@RequestParam String service, @RequestParam String team, @RequestParam String project, @RequestParam double increaseAmount) {
        CostIncrease costIncrease = new CostIncrease(service, team, project, increaseAmount);
        return costAnalysisService.generateRecommendations(costIncrease);
    }
}