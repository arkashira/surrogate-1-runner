package com.axentx.surrogate1.analyzer;

/**
 * Generates a clear, actionable refactoring suggestion for a given concurrency issue.
 */
public class RefactoringSuggester {

    /**
     * Returns a human‑readable suggestion based on the issue description.
     *
     * @param issue the concurrency issue detected by the analyzer
     * @return a suggestion string
     */
    public String suggest(ConcurrencyIssue issue) {
        // The suggestion is already embedded in the issue, but we format it nicely.
        return String.format(
                "Line %d: %s%nSuggested fix: %s",
                issue.getLineNumber(),
                issue.getDescription(),
                issue.getSuggestion()
        );
    }
}