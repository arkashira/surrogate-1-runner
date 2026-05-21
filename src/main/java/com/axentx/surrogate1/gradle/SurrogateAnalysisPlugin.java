package com.axentx.surrogate1.gradle;

import org.gradle.api.Plugin;
import org.gradle.api.Project;

/**
 * Gradle plugin that adds a {@code surrogateAnalysis} task to the project.
 * The task scans Java source files for potential concurrent collection misuse
 * (stub implementation) and generates a concise report.
 */
public class SurrogateAnalysisPlugin implements Plugin<Project> {

    @Override
    public void apply(Project project) {
        // Register the analysis task with sensible defaults.
        project.getTasks().register("surrogateAnalysis", SurrogateAnalysisTask.class, task -> {
            task.setGroup("verification");
            task.setDescription("Analyzes code for concurrent collection misuse.");
            task.getSourceDir().set(project.file("src/main/java"));
            task.getReportFile().set(project.file("build/reports/surrogate-analysis.txt"));
        });
    }
}