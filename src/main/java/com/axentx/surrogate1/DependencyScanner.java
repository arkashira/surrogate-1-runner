package com.axentx.surrogate1;

import org.owasp.dependencycheck.Engine;
import org.owasp.dependencycheck.reporting.ReportGenerator;
import org.owasp.dependencycheck.utils.Settings;

import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;

public class DependencyScanner {
    private static final Logger LOGGER = Logger.getLogger(DependencyScanner.class.getName());

    public void scanDependencies() {
        try {
            Settings settings = new Settings();
            Engine engine = new Engine(settings);
            engine.scan(new File("src/main/resources"));
            engine.analyzeDependencies();
            ReportGenerator reportGenerator = new ReportGenerator(engine.getDependencies(), new File("dependency-check-report.html"), settings);
            reportGenerator.generateReports();
            System.out.println("Dependency scanning completed successfully.");
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Error during dependency scanning", e);
        }
    }

    public static void main(String[] args) {
        new DependencyScanner().scanDependencies();
    }
}