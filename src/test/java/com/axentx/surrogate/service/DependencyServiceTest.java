package com.axentx.surrogate.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class DependencyServiceTest {
    @InjectMocks
    private DependencyService dependencyService;

    @Test
    public void testLogDependencyChange() {
        Logger logger = mock(Logger.class);
        when(LoggerFactory.getLogger(DependencyService.class)).thenReturn(logger);

        dependencyService.logDependencyChange("test-dependency", "1.0.0", "1.1.0");

        verify(logger).info("Dependency change: {} from {} to {}", "test-dependency", "1.0.0", "1.1.0");
    }
}