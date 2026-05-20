package com.axentx.surrogate1.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "profiles")
public class Profile {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String productName;

    @Column(nullable = false)
    private String niche;

    @Column(nullable = false)
    private Integer monthlyUsers;

    @Column(nullable = false)
    private Integer monthlyRevenue;

    @Column(nullable = false)
    private String revenueModel;

    @Column(nullable = false)
    private String targetAudience;

    @Column(nullable = false)
    private String primaryPainPoint;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @Column(nullable = false)
    private String encryptionKeyHash;

    @PrePersist
    protected void onCreate() {
        this.id = UUID.randomUUID();
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
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
    public String getEncryptionKeyHash() { return encryptionKeyHash; }
    public void setEncryptionKeyHash(String encryptionKeyHash) { this.encryptionKeyHash = encryptionKeyHash; }
}