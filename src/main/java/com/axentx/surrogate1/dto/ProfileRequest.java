package com.axentx.surrogate1.dto;

import javax.validation.constraints.NotBlank;

public class ProfileRequest {
    @NotBlank(message = "Niche is required")
    private String niche;

    @NotBlank(message = "Product metrics are required")
    private String productMetrics;

    // Getters and setters
    public String getNiche() {
        return niche;
    }

    public void setNiche(String niche) {
        this.niche = niche;
    }

    public String getProductMetrics() {
        return productMetrics;
    }

    public void setProductMetrics(String productMetrics) {
        this.productMetrics = productMetrics;
    }
}