package com.axentx.surrogate.repository;

import com.axentx.surrogate.model.PipelineIntegration;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface PipelineIntegrationRepository extends JpaRepository<PipelineIntegration, Long> {
    Optional<PipelineIntegration> findByPipelineId(String pipelineId);
}