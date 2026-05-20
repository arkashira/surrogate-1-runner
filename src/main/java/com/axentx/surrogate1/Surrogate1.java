package com.axentx.surrogate1;

import com.axentx.surrogate1.analyzer.ConcurrentCollectionAnalyzer;
import com.axentx.surrogate1.refactor.RefactoringSuggestionEngine;
import java.util.List;

public class Surrogate1 {
    private final ConcurrentCollectionAnalyzer analyzer;
    private final RefactoringSuggestionEngine refactoringEngine;

    public Surrogate1() {
        this.analyzer = new ConcurrentCollectionAnalyzer();
        this.refactoringEngine = new RefactoringSuggestionEngine();
    }

    public void analyzeAndSuggest(String sourceCode) {
        // Analyze for concurrency issues
        List<ConcurrentCollectionAnalyzer.ConcurrencyIssue> issues = analyzer.analyze(sourceCode);

        if (issues.isEmpty()) {
            System.out.println("No concurrency issues detected in the provided code.");
            return;
        }

        System.out.println("Detected " + issues.size() + " concurrency issues:");
        System.out.println("--------------------------------------------");

        // Generate and display refactoring suggestions for each issue
        for (ConcurrentCollectionAnalyzer.ConcurrencyIssue issue : issues) {
            System.out.println("\nIssue: " + issue.getDescription());
            System.out.println("Recommendation: " + issue.getRecommendation());

            List<String> suggestions = refactoringEngine.generateSuggestions(issue);
            System.out.println("\nSuggested Refactorings:");
            for (String suggestion : suggestions) {
                System.out.println("- " + suggestion);
            }
        }
    }

    public static void main(String[] args) {
        Surrogate1 surrogate = new Surrogate1();
        String sampleCode = "public class Test { private Map<String, String> map = new HashMap<>(); }";
        surrogate.analyzeAndSuggest(sampleCode);
    }
}