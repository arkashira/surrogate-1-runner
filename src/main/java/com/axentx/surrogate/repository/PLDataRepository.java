package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.PLData;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;

public interface PLDataRepository extends JpaRepository<PLData, Long> {
    List<PLData> findByDateBetween(LocalDate startDate, LocalDate endDate);
}