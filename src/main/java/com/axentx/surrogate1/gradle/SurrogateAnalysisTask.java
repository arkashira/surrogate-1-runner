package com.axentx.surrogate1.gradle;

import org.gradle.api.DefaultTask;
import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.tasks.*;

import java.io.*;
import java.nio.file.*;
import java.util.stream.Stream;

/**
 * Simple analysis task that walks Java source files and writes a placeholder
 * report. Real analysis logic (detecting overridden default methods in
 * concurrent collections) should replace the stub implementation.
 */
public abstract class SurrogateAnalysisTask extends DefaultTask {

    /** Directory containing Java source files to analyse. */
    @InputDirectory
    public abstract DirectoryProperty getSourceDir();

    /** File where the analysis report will be written. */
    @OutputFile
    public abstract RegularFileProperty getReportFile();

    @TaskAction
    public void analyze() throws IOException {
        Path srcRoot = getSourceDir().getAsFile().get().toPath();
        Path reportPath = getReportFile().getAsFile().get().toPath();

        // Ensure the report directory exists.
        Files.createDirectories(reportPath.getParent());

        try (BufferedWriter writer = Files.newBufferedWriter(reportPath,
                StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {

            if (!Files.isDirectory(srcRoot)) {
                writer.write("Source directory not found: " + srcRoot);
                writer.newLine();
                return;
            }

            // Walk all .java files – placeholder logic.
            try (Stream<Path> files = Files.walk(srcRoot)) {
                files.filter(p -> p.toString().endsWith(".java"))
                     .forEach(p -> {
                         try {
                             // Placeholder: just list the file.
                             writer.write("Analyzed: " + srcRoot.relativize(p));
                             writer.newLine();
                         } catch (IOException e) {
                             throw new UncheckedIOException(e);
                         }
                     });
            }

            // Add a footer indicating this is a stub report.
            writer.write("---");
            writer.newLine();
            writer.write("NOTE: This is a stub implementation. Replace with real analysis logic.");
            writer.newLine();
        }
    }
}