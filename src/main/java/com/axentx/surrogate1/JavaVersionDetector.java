package com.axentx.surrogate1;

import java.util.logging.Level;
import java.util.logging.Logger;

public class JavaVersionDetector {
    private static final Logger logger = Logger.getLogger(JavaVersionDetector.class.getName());

    public static String getJavaVersion() {
        String version = System.getProperty("java.version");
        logger.log(Level.INFO, "Detected Java version: " + version);
        return version;
    }

    public static boolean isJavaVersionSupported(String version) {
        // Check if the Java version is supported
        // For example, KiCAD 9 requires Java 8 or higher
        return version.startsWith("1.8") || version.startsWith("11") || version.startsWith("17");
    }

    public static void checkAndHandleJavaVersion() {
        String javaVersion = getJavaVersion();
        if (!isJavaVersionSupported(javaVersion)) {
            logger.log(Level.SEVERE, "Unsupported Java version: " + javaVersion);
            // Handle the unsupported Java version, e.g., provide a fallback or exit
            System.exit(1);
        }
    }
}