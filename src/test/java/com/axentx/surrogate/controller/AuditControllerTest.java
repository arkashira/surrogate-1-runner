package com.axentx.surrogate.controller;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.assertNotNull;

@ExtendWith(MockitoExtension.class)
public class AuditControllerTest {
    @InjectMocks
    private AuditController auditController;

    @Test
    public void testGetAuditLogs() throws IOException {
        String logs = auditController.getAuditLogs();
        assertNotNull(logs);
    }
}