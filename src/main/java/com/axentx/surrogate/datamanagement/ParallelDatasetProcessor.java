package com.axentx.surrogate.datamanagement;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Objects;
import java.util.concurrent.ForkJoinPool;
import java.util.function.Function;
import java.util.stream.Stream;

/**
 * Utility for processing large dataset files in parallel.
 *
 * <p>The processor works on a line‑by‑line basis.  Each line is handed to a
 * {@link DataRecordProcessor} which returns the transformed line (or {@code null}
 * to drop the record).  The transformed lines are written to the output file
 * preserving the original order of the input lines as much as possible while
 * still benefiting from parallel execution.
 *
 * <p>Typical usage:
 *
 * <pre>{@code
 * Path in = Paths.get("large_dataset.txt");
 * Path out = Paths.get("processed.txt");
 * ParallelDatasetProcessor.process(in, out,
 *     record -> record.toUpperCase(),   // simple example processor
 *     Runtime.getRuntime().availableProcessors());
 * }</pre>
 *
 * <p>The implementation uses a custom {@link ForkJoinPool} to avoid
 * interfering with the global common pool, which is important when the
 * surrounding application also relies on parallel streams.
 *
 * @author AxentX
 */
public final class ParallelDatasetProcessor {

    private ParallelDatasetProcessor() {
        // utility class – prevent instantiation
    }

    /**
     * Functional interface for processing a single record (a line of text).
     */
    @FunctionalInterface
    public interface DataRecordProcessor extends Function<String, String> {
        /**
         * Process a single record.
         *
         * @param record the raw input line; never {@code null}
         * @return the transformed line, or {@code null} to omit the record
         */
        @Override
        String apply(String record);
    }

    /**
     * Processes the input file in parallel and writes the transformed records
     * to the output file.
     *
     * @param inputPath   path to the source dataset (plain‑text, line delimited)
     * @param outputPath  path where the processed dataset will be written
     * @param processor   user‑provided record processor
     * @param parallelism desired level of parallelism; if less than 1 the
     *                    number of available processors is used
     * @throws IOException if an I/O error occurs
     */
    public static void process(
            Path inputPath,
            Path outputPath,
            DataRecordProcessor processor,
            int parallelism) throws IOException {

        Objects.requireNonNull(inputPath, "inputPath must not be null");
        Objects.requireNonNull(outputPath, "outputPath must not be null");
        Objects.requireNonNull(processor, "processor must not be null");

        int threads = parallelism > 0 ? parallelism
                : Runtime.getRuntime().availableProcessors();

        // Ensure parent directories exist
        Files.createDirectories(outputPath.getParent());

        // Use a dedicated ForkJoinPool so we don't pollute the global common pool
        ForkJoinPool forkJoinPool = new ForkJoinPool(threads);
        try (BufferedWriter writer = Files.newBufferedWriter(outputPath)) {
            // The writer is shared; we synchronize writes to preserve line integrity.
            forkJoinPool.submit(() -> {
                try (Stream<String> lines = Files.lines(inputPath)) {
                    lines.parallel()
                         .map(processor)
                         .filter(Objects::nonNull)
                         .forEachOrdered(record -> {
                             // forEachOrdered preserves encounter order within the
                             // parallel stream, which keeps output deterministic.
                             synchronized (writer) {
                                 try {
                                     writer.write(record);
                                     writer.newLine();
                                 } catch (IOException e) {
                                     throw new UncheckedIOException(e);
                                 }
                             }
                         });
                } catch (IOException e) {
                    throw new UncheckedIOException(e);
                }
            }).join(); // wait for completion
        } finally {
            forkJoinPool.shutdown();
        }
    }
}