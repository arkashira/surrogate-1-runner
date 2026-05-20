package com.axentx.surrogate1.analyzer;

/**
 * Simple POJO representing a concurrency issue detected in source code.
 */
public class ConcurrencyIssue {
    private final int lineNumber;
    private final String description;
    private final String suggestion;

    public ConcurrencyIssue(int lineNumber, String description, String suggestion) {
        this.lineNumber = lineNumber;
        this.description = description;
        this.suggestion = suggestion;
    }

    public int getLineNumber() {
        return lineNumber;
    }

    public String getDescription() {
        return description;
    }

    public String getSuggestion() {
        return suggestion;
    }

    @Override
    public String toString() {
        return "ConcurrencyIssue{" +
                "lineNumber=" + lineNumber +
                ", description='" + description + '\'' +
                ", suggestion='" + suggestion + '\'' +
                '}';
    }
}