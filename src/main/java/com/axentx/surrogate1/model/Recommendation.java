package com.axentx.surrogate1.model;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Map;
import java.util.Objects;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

public class Recommendation {

    private static final Map<String, BigDecimal> INSTANCE_HOURLY_RATES = Map.of(
            "m5.large",  new BigDecimal("0.096"),
            "m5.xlarge", new BigDecimal("0.192"),
            "m5.2xlarge", new BigDecimal("0.384"),
            "t3.medium", new BigDecimal("0.0416"),
            "t3.large",  new BigDecimal("0.0832")
    );

    private static final double UNDERUTILIZATION_THRESHOLD = 0.80;
    private static final int HOURS_IN_MONTH = 730;

    private final String currentInstanceType;
    private final String region;
    private final BigDecimal currentMonthlyCost;
    private final String recommendedInstanceType;
    private final BigDecimal recommendedMonthlyCost;
    private final BigDecimal savingsEstimate;
    private final String description;
    private final String applyUrl;
    private final double utilizationPercentage;

    public Recommendation(String currentInstanceType, String region, double utilizationPercentage) {
        this.currentInstanceType = Objects.requireNonNull(currentInstanceType);
        this.region = Objects.requireNonNull(region);
        this.utilizationPercentage = validateUtilizationPercentage(utilizationPercentage);

        this.currentMonthlyCost = estimateMonthlyCost(this.currentInstanceType);
        this.recommendedInstanceType = findRecommendedInstance(this.currentInstanceType, this.utilizationPercentage);
        this.recommendedMonthlyCost = estimateMonthlyCost(this.recommendedInstanceType);
        this.savingsEstimate = this.currentMonthlyCost.subtract(this.recommendedMonthlyCost)
                .setScale(2, RoundingMode.HALF_UP);
        this.description = generateDescription();
        this.applyUrl = buildApplyUrl();
    }

    private double validateUtilizationPercentage(double utilizationPercentage) {
        if (utilizationPercentage < 0 || utilizationPercentage > 1) {
            throw new IllegalArgumentException("Utilization percentage must be between 0 and 1");
        }
        return utilizationPercentage;
    }

    private BigDecimal estimateMonthlyCost(String instanceType) {
        BigDecimal hourly = INSTANCE_HOURLY_RATES.getOrDefault(instanceType, BigDecimal.ZERO);
        return hourly.multiply(BigDecimal.valueOf(HOURS_IN_MONTH)).setScale(2, RoundingMode.HALF_UP);
    }

    private String findRecommendedInstance(String current, double utilization) {
        if (utilization < UNDERUTILIZATION_THRESHOLD) {
            return switch (current) {
                case "m5.large" -> "m5.xlarge";
                case "m5.xlarge" -> "m5.2xlarge";
                case "t3.large" -> "t3.medium";
                default -> current;
            };
        }
        return current;
    }

    private String generateDescription() {
        return String.format("%s in %s is over-provisioned (%.0f%% utilization) and can be reduced to %s",
                currentInstanceType, region, utilizationPercentage * 100, recommendedInstanceType);
    }

    private String buildApplyUrl() {
        return String.format("https://costinel.example.com/apply?instance=%s&region=%s",
                currentInstanceType, region);
    }

    // Getters

    public String getCurrentInstanceType() {
        return currentInstanceType;
    }

    public String getRegion() {
        return region;
    }

    public BigDecimal getCurrentMonthlyCost() {
        return currentMonthlyCost;
    }

    public String getRecommendedInstanceType() {
        return recommendedInstanceType;
    }

    public BigDecimal getRecommendedMonthlyCost() {
        return recommendedMonthlyCost;
    }

    public BigDecimal getSavingsEstimate() {
        return savingsEstimate;
    }

    public String getDescription() {
        return description;
    }

    public String getApplyUrl() {
        return applyUrl;
    }

    public double getUtilizationPercentage() {
        return utilizationPercentage;
    }

    @Override
    public String toString() {
        return String.format("Recommendation[%s in %s -> %s, savings: $%s/month, apply: %s]",
                currentInstanceType, region, recommendedInstanceType, savingsEstimate, applyUrl);
    }

    // Tests

    public static void main(String[] args) {
        Recommendation recommendation = new Recommendation("m5.large", "us-west-2", 0.5);
        assertEquals("m5.xlarge", recommendation.getRecommendedInstanceType());
        assertEquals(new BigDecimal("35.28"), recommendation.getSavingsEstimate());

        Recommendation highUtilization = new Recommendation("t3.large", "us-east-1", 0.9);
        assertEquals("t3.large", highUtilization.getRecommendedInstanceType());
        assertEquals(BigDecimal.ZERO, highUtilization.getSavingsEstimate());

        Recommendation unknownInstance = new Recommendation("unknown", "us-central-1", 0.6);
        assertEquals("unknown", unknownInstance.getRecommendedInstanceType());
        assertEquals(BigDecimal.ZERO, unknownInstance.getSavingsEstimate());

        assertNotEquals(recommendation, highUtilization);
        assertNotEquals(recommendation, unknownInstance);
    }
}