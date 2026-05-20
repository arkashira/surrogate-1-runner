package com.axentx.surrogate.dto;

import java.math.BigDecimal;

public record TopCostDriverDto(
        String vmType,
        String region,
        int instanceCount,
        BigDecimal totalCost
) {}