package com.axentx.surrogate.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import com.axentx.surrogate.model.SyntheticDataGenerator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class SyntheticDataServiceTest {

    @Mock
    private SyntheticDataGenerator syntheticDataGenerator;

    @InjectMocks
    private SyntheticDataService syntheticDataService;

    @Test
    public void generateSyntheticData_shouldReturnGeneratedData() {
        when(syntheticDataGenerator.generate("datadog")).thenReturn("{\"metric\": \"datadog.metric\", \"value\": 42}");

        String result = syntheticDataService.generateSyntheticData("datadog");

        assertEquals("{\"metric\": \"datadog.metric\", \"value\": 42}", result);
    }
}