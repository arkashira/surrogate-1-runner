package com.axentx.surrogate.model;

import javax.persistence.*;

@Entity
public class CostAnalysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "cost_increase_id")
    private CostIncrease costIncrease;

    private String rootCause;
    private String recommendation;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public CostIncrease getCostIncrease() {
        return costIncrease;
    }

    public void setCostIncrease(CostIncrease costIncrease) {
        this.costIncrease = costIncrease;
    }

    public String getRootCause() {
        return rootCause;
    }

    public void setRootCause(String rootCause) {
        this.rootCause = rootCause;
    }

    public String getRecommendation() {
        return recommendation;
    }

    public void setRecommendation(String recommendation) {
        this.recommendation = recommendation;
    }
}