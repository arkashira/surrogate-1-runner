package com.axentx.surrogate.model;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class SyntheticDataGeneratorTest {

    private final SyntheticDataGenerator syntheticDataGenerator = new SyntheticDataGenerator();

    @Test
    public void generate_shouldReturnSyntheticDataForValidIntegrationType() {
        String result = syntheticDataGenerator.generate("datadog");

        assertNotNull(result);
    }

    @Test
    public void generate_shouldThrowExceptionForInvalidIntegrationType() {
        assertThrows(IllegalArgumentException.class, () -> syntheticDataGenerator.generate("invalid"));
    }
}