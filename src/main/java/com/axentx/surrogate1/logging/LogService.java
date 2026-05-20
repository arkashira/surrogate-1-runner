package com.axentx.surrogate1.logging;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class LogService {

    private static final Logger logger = LoggerFactory.getLogger(LogService.class);
    private static final Map<String, AuthenticationLog> authLogStore = new ConcurrentHashMap<>();

    public static class AuthenticationLog {
        private final String username;
        private final Instant timestamp;
        private final String status;
        private final String ipAddress;
        private final String userAgent;

        public AuthenticationLog(String username, String status, String ipAddress, String userAgent) {
            this.username = username;
            this.timestamp = Instant.now();
            this.status = status;
            this.ipAddress = ipAddress;
            this.userAgent = userAgent;
        }

        public String getUsername() { return username; }
        public Instant getTimestamp() { return timestamp; }
        public String getStatus() { return status; }
        public String getIpAddress() { return ipAddress; }
        public String getUserAgent() { return userAgent; }
    }

    public void logAuthenticationAttempt(String username, boolean success, String ipAddress, String userAgent) {
        String status = success ? "SUCCESS" : "FAILED";
        AuthenticationLog log = new AuthenticationLog(username, status, ipAddress, userAgent);
        authLogStore.put(username, log);

        if (success) {
            logger.info("AUTH_SUCCESS: user={}, timestamp={}, ip={}, ua={}", 
                username, timestamp, ipAddress, userAgent);
        } else {
            logger.warn("AUTH_FAILED: user={}, timestamp={}, ip={}, ua={}", 
                username, timestamp, ipAddress, userAgent);
        }
    }

    public AuthenticationLog getAuthLog(String username) {
        return authLogStore.get(username);
    }

    public void clearAuthLog(String username) {
        authLogStore.remove(username);
    }

    public Map<String, AuthenticationLog> getAllAuthLogs() {
        return new ConcurrentHashMap<>(authLogStore);
    }
}