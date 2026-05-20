package com.axentx.surrogate.model;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "pipeline_integrations")
public class PipelineIntegration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String pipelineType;
    private String pipelineId;
    private String status;
    private Instant createdAt;

    protected PipelineIntegration() { /* JPA */ }

    public PipelineIntegration(String pipelineType, String pipelineId, String status) {
        this.pipelineType = pipelineType;
        this.pipelineId = pipelineId;
        this.status = status;
        this.createdAt = Instant.now();
    }

    // Getters only – immutable after creation
    public Long getId() { return id; }
    public String getPipelineType() { return pipelineType; }
    public String getPipelineId() { return pipelineId; }
    public String getStatus() { return status; }
    public Instant getCreatedAt() { return createdAt; }
}