package com.axentx.surrogate1.model;

public class StrategyRequest {
    private String businessDetails;
    private String goals;

    // Getters and setters
    public String getBusinessDetails() {
        return businessDetails;
    }

    public void setBusinessDetails(String businessDetails) {
        this.businessDetails = businessDetails;
    }

    public String getGoals() {
        return goals;
    }

    public void setGoals(String goals) {
        this.goals = goals;
    }

    @Override
    public String toString() {
        return "StrategyRequest{" +
                "businessDetails='" + businessDetails + '\'' +
                ", goals='" + goals + '\'' +
                '}';
    }
}