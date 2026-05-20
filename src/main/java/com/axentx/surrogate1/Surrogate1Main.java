package com.axentx.surrogate1;

import java.util.logging.Level;
import java.util.logging.Logger;

public class Surrogate1Main {
    private static final Logger logger = Logger.getLogger(Surrogate1Main.class.getName());

    public static void main(String[] args) {
        try {
            // Check Java version before initializing KiCAD
            JavaVersionDetector.checkAndHandleJavaVersion();

            // Initialize KiCAD and other components
            logger.log(Level.INFO, "Initializing Surrogate-1 with KiCAD 9");
            // Add your initialization code here
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Failed to initialize Surrogate-1", e);
        }
    }
}