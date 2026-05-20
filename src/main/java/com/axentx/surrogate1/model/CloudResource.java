package com.axentx.surrogate1.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CloudResource {

    private String resourceId;

    @NotBlank(message = "Resource name is required")
    private String resourceName;

    @Positive(message = "Cost must be positive")
    private double cost;

    @Positive(message = "Utilization must be positive")
    private double utilization;
}