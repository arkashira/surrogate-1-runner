package com.axentx.surrogate1.analyzer;

import java.util.ArrayList;
import java.util.List;

public class ConcurrentCollectionAnalyzer {

    public List<ConcurrencyIssue> analyze(String sourceCode) {
        List<ConcurrencyIssue> issues = new ArrayList<>();

        // Detect common concurrency issues in collections
        if (sourceCode.contains("new HashMap<>()") && !sourceCode.contains("ConcurrentHashMap")) {
            issues.add(new ConcurrencyIssue(
                "Non-thread-safe HashMap usage detected",
                "HashMap is not thread-safe. Consider using ConcurrentHashMap for concurrent access.",
                "Replace HashMap with ConcurrentHashMap in multi-threaded environments"
            ));
        }

        if (sourceCode.contains("new ArrayList<>()") && !sourceCode.contains("CopyOnWriteArrayList")) {
            issues.add(new ConcurrencyIssue(
                "Non-thread-safe ArrayList usage detected",
                "ArrayList is not thread-safe. Consider using CopyOnWriteArrayList for concurrent access.",
                "Replace ArrayList with CopyOnWriteArrayList when multiple threads may access the list"
            ));
        }

        // Add more collection type checks as needed
        if (sourceCode.contains("new Hashtable<>()") && !sourceCode.contains("ConcurrentHashMap")) {
            issues.add(new ConcurrencyIssue(
                "Legacy Hashtable usage detected",
                "Hashtable is synchronized but generally slower than ConcurrentHashMap.",
                "Consider migrating to ConcurrentHashMap for better performance"
            ));
        }

        return issues;
    }

    public static class ConcurrencyIssue {
        private final String description;
        private final String recommendation;
        private final String rationale;

        public ConcurrencyIssue(String description, String recommendation, String rationale) {
            this.description = description;
            this.recommendation = recommendation;
            this.rationale = rationale;
        }

        public String getDescription() {
            return description;
        }

        public String getRecommendation() {
            return recommendation;
        }

        public String getRationale() {
            return rationale;
        }
    }
}