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

    public List<CostIncrease> getCostIncreases() {
        return costAnalysisRepository.findAllCostIncreases();
    }

    public CostAnalysis getRootCauseAnalysis(Long costIncreaseId) {
        return costAnalysisRepository.findRootCauseAnalysisById(costIncreaseId);
    }

    public void saveCostAnalysis(CostAnalysis costAnalysis) {
        costAnalysisRepository.save(costAnalysis);
    }
}