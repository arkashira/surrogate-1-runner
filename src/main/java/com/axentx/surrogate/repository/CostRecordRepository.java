package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.CostRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface CostRecordRepository extends JpaRepository<CostRecord, Long> {

    @Query(value =
        "SELECT vm_type AS vmType, region, SUM(instance_count) AS instanceCount, " +
        "       SUM(total_cost) AS totalCost " +
        "FROM cost_record " +
        "WHERE date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY) " +
        "GROUP BY vm_type, region " +
        "ORDER BY totalCost DESC " +
        "LIMIT 3", nativeQuery = true)
    List<Object[]> findTopCostDriversRaw();
}