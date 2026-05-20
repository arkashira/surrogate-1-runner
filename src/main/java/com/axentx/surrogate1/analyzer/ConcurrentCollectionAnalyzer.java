package com.axentx.surrogate1.analyzer;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Very lightweight static analyzer that looks for instantiations of non‑thread‑safe
 * collection classes and produces {@link ConcurrencyIssue}s with refactoring suggestions.
 *
 * This implementation is deliberately simple: it scans the source line‑by‑line,
 * matches known non‑concurrent collection constructors, and suggests the most
 * appropriate concurrent alternative.
 */
public class ConcurrentCollectionAnalyzer {

    // Patterns for non‑thread‑safe collections we care about.
    private static final Pattern ARRAYLIST_PATTERN = Pattern.compile("\\bnew\\s+ArrayList\\s*<[^>]*>\\s*\\(");
    private static final Pattern LINKEDLIST_PATTERN = Pattern.compile("\\bnew\\s+LinkedList\\s*<[^>]*>\\s*\\(");
    private static final Pattern HASHMAP_PATTERN = Pattern.compile("\\bnew\\s+HashMap\\s*<[^>]*>\\s*\\(");
    private static final Pattern HASHSET_PATTERN = Pattern.compile("\\bnew\\s+HashSet\\s*<[^>]*>\\s*\\(");

    /**
     * Analyzes a Java source file (provided as a single {@code String}) and returns a list of
     * concurrency issues with actionable suggestions.
     *
     * @param sourceCode the full Java source code to analyze
     * @return list of detected {@link ConcurrencyIssue}s; empty if none found
     */
    public List<ConcurrencyIssue> analyze(String sourceCode) {
        List<ConcurrencyIssue> issues = new ArrayList<>();

        String[] lines = sourceCode.split("\\R"); // split on any line terminator
        for (int i = 0; i < lines.length; i++) {
            String line = lines[i];

            Matcher m;
            if ((m = ARRAYLIST_PATTERN.matcher(line)).find()) {
                issues.add(new ConcurrencyIssue(
                        i + 1,
                        "Usage of non‑thread‑safe ArrayList",
                        "Replace with java.util.concurrent.CopyOnWriteArrayList or Collections.synchronizedList"
                ));
            } else if ((m = LINKEDLIST_PATTERN.matcher(line)).find()) {
                issues.add(new ConcurrencyIssue(
                        i + 1,
                        "Usage of non‑thread‑safe LinkedList",
                        "Replace with java.util.concurrent.CopyOnWriteArrayList if random access is needed, or use a synchronized wrapper"
                ));
            } else if ((m = HASHMAP_PATTERN.matcher(line)).find()) {
                issues.add(new ConcurrencyIssue(
                        i + 1,
                        "Usage of non‑thread‑safe HashMap",
                        "Replace with java.util.concurrent.ConcurrentHashMap"
                ));
            } else if ((m = HASHSET_PATTERN.matcher(line)).find()) {
                issues.add(new ConcurrencyIssue(
                        i + 1,
                        "Usage of non‑thread‑safe HashSet",
                        "Replace with java.util.concurrent.ConcurrentSkipListSet or Collections.newSetFromMap(new ConcurrentHashMap<>())"
                ));
            }
        }

        return issues;
    }
}