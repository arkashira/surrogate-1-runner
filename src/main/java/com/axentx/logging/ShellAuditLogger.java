package com.axentx.logging;

import com.axentx.utils.UserUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class ShellAuditLogger {
    private static final Logger logger = LoggerFactory.getLogger(ShellAuditLogger.class);
    private static final String LOG_DIR = "/var/log/axentx/surrogate-shell/";
    private static final String LOG_FILE = LOG_DIR + Instant.now().toEpochMilli() + ".jsonl";

    public void logCommand(String command, String userId, String containerId) {
        Map<String, String> logEntry = new HashMap<>();
        logEntry.put("timestamp", Instant.now().toString());
        logEntry.put("userId", userId);
        logEntry.put("containerId", containerId);
        logEntry.put("command", command);

        try (PrintWriter out = new PrintWriter(new FileWriter(LOG_FILE, true))) {
            out.println(new org.json.JSONObject(logEntry).toString());
        } catch (IOException e) {
            logger.error("Error writing log entry", e);
        }
    }

    public static void main(String[] args) {
        ShellAuditLogger logger = new ShellAuditLogger();
        String userId = UserUtils.getCurrentUserId();
        String containerId = System.getenv("CONTAINER_ID");

        // Simulate command execution and logging
        logger.logCommand("ls -la", userId, containerId);
        logger.logCommand("cat /etc/hosts", userId, containerId);
    }
}