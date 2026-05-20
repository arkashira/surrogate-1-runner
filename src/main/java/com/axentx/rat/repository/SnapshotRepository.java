package com.axentx.rat.repository;

import com.axentx.rat.model.SnapshotEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SnapshotRepository extends JpaRepository<SnapshotEntity, Long> {
    // No custom methods needed for the current service implementation
}