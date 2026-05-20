package com.axentx.rat.service;

import com.axentx.rat.dto.BalanceResponse;
import com.axentx.rat.model.SnapshotEntity;
import com.axentx.rat.repository.SnapshotRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class BalanceService {

    private final SnapshotRepository snapshotRepository;

    public BalanceService(SnapshotRepository snapshotRepository) {
        this.snapshotRepository = snapshotRepository;
    }

    public BalanceResponse getConsolidatedBalance() {
        List<SnapshotEntity> allSnapshots = snapshotRepository.findAll();

        if (allSnapshots.isEmpty()) {
            return new BalanceResponse(BigDecimal.ZERO, Instant.now());
        }

        // Determine the most recent snapshot date
        Optional<LocalDate> mostRecentDateOpt = allSnapshots.stream()
                .map(SnapshotEntity::getSnapshotDate)
                .max(LocalDate::compareTo);

        LocalDate mostRecentDate = mostRecentDateOpt.orElse(LocalDate.now());

        // Sum balances for that date
        BigDecimal total = allSnapshots.stream()
                .filter(s -> mostRecentDate.equals(s.getSnapshotDate()))
                .map(SnapshotEntity::getBalanceUsd)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        // Use the latest timestamp among the selected snapshots as last_updated
        Instant lastUpdated = allSnapshots.stream()
                .filter(s -> mostRecentDate.equals(s.getSnapshotDate()))
                .map(SnapshotEntity::getUpdatedAt)
                .max(Instant::compareTo)
                .orElse(Instant.now());

        return new BalanceResponse(total, lastUpdated);
    }
}