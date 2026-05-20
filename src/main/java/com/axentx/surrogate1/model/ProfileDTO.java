package com.axentx.surrogate1.model;

import java.time.LocalDateTime;

public class ProfileDTO {

    private UUID id;
    private String email;
    private String productName;
    private String niche;
    private Integer monthlyUsers;
    private Integer monthlyRevenue;
    private String revenueModel;
    private String targetAudience;
    private String primaryPainPoint;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public ProfileDTO() {}

    public ProfileDTO(Profile profile) {
        this.id = profile.getId();
        this.email = profile.getEmail();
        this.productName = profile.getProductName();
        this.niche = profile.getNiche();
        this.monthlyUsers = profile.getMonthlyUsers();
        this.monthlyRevenue = profile.getMonthlyRevenue();
        this.revenueModel = profile.getRevenueModel();
        this.targetAudience = profile.getTargetAudience();
        this.primaryPainPoint = profile.getPrimaryPainPoint();
        this.createdAt = profile.getCreatedAt();
        this.updatedAt = profile.getUpdatedAt();
    }

    // Getters and Setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public String getNiche() { return niche; }
    public void setNiche(String niche) { this.niche = niche; }
    public Integer getMonthlyUsers() { return monthlyUsers; }
    public void setMonthlyUsers(Integer monthlyUsers) { this.monthlyUsers = monthlyUsers; }
    public Integer getMonthlyRevenue() { return monthlyRevenue; }
    public void setMonthlyRevenue(Integer monthlyRevenue) { this.monthlyRevenue = monthlyRevenue; }
    public String getRevenueModel() { return revenueModel; }
    public void setRevenueModel(String revenueModel) { this.revenueModel = revenueModel; }
    public String getTargetAudience() { return targetAudience; }
    public void setTargetAudience(String targetAudience) { this.targetAudience = targetAudience; }
    public String getPrimaryPainPoint() { return primaryPainPoint; }
    public void setPrimaryPainPoint(String primaryPainPoint) { this.primaryPainPoint = primaryPainPoint; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}