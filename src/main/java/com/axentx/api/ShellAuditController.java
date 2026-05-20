package com.axentx.api;

import com.axentx.logging.ShellAuditLogger;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

@RestController
public class ShellAuditController {

    @GetMapping("/api/shell-audit")
    public List<String> getLastTenSessions() throws IOException {
        List<String> logFiles = Files.list(Paths.get("/var/log/axentx/surrogate-shell/"))
                .sorted((a, b) -> Long.compare(Paths.get(b.toString()).getFileName().toString(), Paths.get(a.toString()).getFileName().toString()))
                .limit(10)
                .map(Paths::getFileName)
                .map(Paths::toString)
                .collect(Collectors.toList());

        return logFiles;
    }
}