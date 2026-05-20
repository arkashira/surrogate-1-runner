package com.axentx.surrogate.service;

import com.axentx.surrogate.model.CostAnalysis;
import com.axentx.surrogate.model.CostIncrease;
import com.axentx.surrogate.repository.CostAnalysisRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CostAnalysisService {

    @Autowired
    private CostAnalysisRepository costAnalysisRepository;

    public List<CostAnalysis> getCostAnalysis() {
        return costAnalysisRepository.findAll();
    }

    public CostAnalysis saveCostAnalysis(CostAnalysis costAnalysis) {
        return costAnalysisRepository.save(costAnalysis);
    }

    public List<CostIncrease> getCostIncreases() {
        return costAnalysisRepository.findCostIncreases();
    }

    public List<String> generateRecommendations(CostIncrease costIncrease) {
        // Generate actionable recommendations based on the cost increase
        // This is a placeholder for the actual recommendation logic
        // The logic should be based on the type of cost increase and the service/team/project involved
        // For example, if the cost increase is due to high usage of a particular service, recommend optimizing the service usage
        // If the cost increase is due to a particular team, recommend reviewing the team's spending and setting up spending limits
        // If the cost increase is due to a particular project, recommend reviewing the project's spending and setting up spending limits

        // For now, return a generic recommendation
        return List.of("Review the spending and set up spending limits");
    }
}