package com.axentx.surrogate.model;

import java.time.Instant;

public record AgentResult(
        String name,
        boolean success,
        String message,
        Object payload,
        Instant startedAt,
        Instant finishedAt
) {}