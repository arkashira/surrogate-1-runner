package com.axentx.surrogate1.freerouter;

import java.io.IOException;
import java.util.Properties;

public class FreerouterWrapper {
    private Properties properties;

    public FreerouterWrapper() {
        properties = new Properties();
        try {
            properties.load(getClass().getClassLoader().getResourceAsStream("application.properties"));
        } catch (IOException e) {
            logError("Failed to load application properties", e);
        }
    }

    public void initialize() {
        String javaVersion = System.getProperty("java.version");
        if (!isCompatibleJavaVersion(javaVersion)) {
            logError("Incompatible Java version: " + javaVersion);
            throw new RuntimeException("Incompatible Java version: " + javaVersion);
        }
        // Additional initialization logic
    }

    private boolean isCompatibleJavaVersion(String version) {
        // Check if the version is compatible with KiCAD 9
        return version.startsWith("1.8") || version.startsWith("9");
    }

    private void logError(String message, Exception e) {
        // Implement logging logic here
        System.err.println(message + ": " + e.getMessage());
    }

    // Other existing methods remain unchanged
}