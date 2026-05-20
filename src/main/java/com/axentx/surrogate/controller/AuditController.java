package com.axentx.surrogate.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@RestController
@RequestMapping("/api/audit")
public class AuditController {

    @GetMapping("/logs")
    public String getAuditLogs() throws IOException {
        return new String(Files.readAllBytes(Paths.get("/var/log/axentx/audit.log")));
    }
}