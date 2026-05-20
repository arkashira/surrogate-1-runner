package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.CostAnalysis;
import com.axentx.surrogate.model.CostIncrease;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CostAnalysisRepository extends JpaRepository<CostAnalysis, Long> {

    @Query("SELECT ci FROM CostIncrease ci WHERE ci.costIncreasePercentage > 0")
    List<CostIncrease> findAllCostIncreases();

    @Query("SELECT ca FROM CostAnalysis ca WHERE ca.costIncrease.id = :costIncreaseId")
    CostAnalysis findRootCauseAnalysisById(Long costIncreaseId);
}