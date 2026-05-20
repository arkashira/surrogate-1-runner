package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.CostAnalysis;
import com.axentx.surrogate.model.CostIncrease;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface CostAnalysisRepository extends JpaRepository<CostAnalysis, Long> {

    @Query("SELECT new com.axentx.surrogate.model.CostIncrease(c.service, c.team, c.project, c.cost - c.previousCost) " +
           "FROM CostAnalysis c WHERE c.cost > c.previousCost")
    List<CostIncrease> findCostIncreases();
}