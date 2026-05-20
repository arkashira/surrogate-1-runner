package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.SpendingAnomaly;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SpendingAnomalyRepository extends JpaRepository<SpendingAnomaly, Long> {

    @Query("SELECT s FROM SpendingAnomaly s WHERE s.date >= CURRENT_DATE - 1")
    List<SpendingAnomaly> findRecentAnomalies();
}