package com.axentx.surrogate.model;

public class CostIncrease {

    private String service;
    private String team;
    private String project;
    private double increaseAmount;

    public CostIncrease(String service, String team, String project, double increaseAmount) {
        this.service = service;
        this.team = team;
        this.project = project;
        this.increaseAmount = increaseAmount;
    }

    // Getters and setters
    public String getService() {
        return service;
    }

    public void setService(String service) {
        this.service = service;
    }

    public String getTeam() {
        return team;
    }

    public void setTeam(String team) {
        this.team = team;
    }

    public String getProject() {
        return project;
    }

    public void setProject(String project) {
        this.project = project;
    }

    public double getIncreaseAmount() {
        return increaseAmount;
    }

    public void setIncreaseAmount(double increaseAmount) {
        this.increaseAmount = increaseAmount;
    }
}