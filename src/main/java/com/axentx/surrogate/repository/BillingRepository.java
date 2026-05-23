package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.BillingInformation;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BillingRepository extends JpaRepository<BillingInformation, Long> {
}