package com.axentx.surrogate.session;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.util.HashMap;
import java.util.Map;

@Component
public class SessionConfigurator {

    @Autowired
    private Environment env;

    private Map<String, String> sessionProperties;

    @PostConstruct
    public void init() {
        sessionProperties = new HashMap<>();
        sessionProperties.put("session.timeout", env.getProperty("session.timeout", "30m"));
        sessionProperties.put("session.max.retry", env.getProperty("session.max.retry", "3"));
        sessionProperties.put("session.optimization.enabled", env.getProperty("session.optimization.enabled", "true"));
        sessionProperties.put("session.monitoring.enabled", env.getProperty("session.monitoring.enabled", "true"));
    }

    public String getProperty(String key) {
        return sessionProperties.get(key);
    }

    public void updateProperty(String key, String value) {
        sessionProperties.put(key, value);
    }

    public void optimizeSession() {
        if (Boolean.parseBoolean(sessionProperties.get("session.optimization.enabled"))) {
            // Implement session optimization logic here
            System.out.println("Optimizing session...");
        }
    }

    public void monitorSession() {
        if (Boolean.parseBoolean(sessionProperties.get("session.monitoring.enabled"))) {
            // Implement session monitoring logic here
            System.out.println("Monitoring session...");
        }
    }
}