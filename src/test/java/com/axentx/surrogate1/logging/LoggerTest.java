package com.axentx.surrogate1.logging;

import org.junit.jupiter.api.Test;

import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.Logger;

import static org.mockito.Mockito.*;

public class LoggerTest {
    @Test
    public void testLogCriticalEvent() {
        Logger mockLogger = mock(Logger.class);
        Logger.logger = mockLogger;

        Logger.logCriticalEvent("Test critical event");

        verify(mockLogger).log(eq(Level.SEVERE), eq("CRITICAL EVENT: Test critical event"));
    }

    @Test
    public void testLogError() {
        Logger mockLogger = mock(Logger.class);
        Logger.logger = mockLogger;

        Exception exception = new Exception("Test error");
        Logger.logError("Test error message", exception);

        verify(mockLogger).log(eq(Level.SEVERE), eq("ERROR: Test error message"), eq(exception));
    }

    @Test
    public void testLogInfo() {
        Logger mockLogger = mock(Logger.class);
        Logger.logger = mockLogger;

        Logger.logInfo("Test info message");

        verify(mockLogger).log(eq(Level.INFO), eq("INFO: Test info message"));
    }

    @Test
    public void testLogWarning() {
        Logger mockLogger = mock(Logger.class);
        Logger.logger = mockLogger;

        Logger.logWarning("Test warning message");

        verify(mockLogger).log(eq(Level.WARNING), eq("WARNING: Test warning message"));
    }
}