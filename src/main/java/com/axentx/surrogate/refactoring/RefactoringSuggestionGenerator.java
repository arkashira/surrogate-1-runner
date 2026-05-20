package com.axentx.surrogate.refactoring;

import java.util.List;
import java.util.ArrayList;

public class RefactoringSuggestionGenerator {

    public List<String> generateSuggestions(String code) {
        List<String> suggestions = new ArrayList<>();

        // Check for concurrency issues
        if (code.contains("synchronized")) {
            suggestions.add("Consider using concurrent collections instead of synchronized blocks.");
        }

        // Check for performance issues
        if (code.contains("for (int i = 0; i < ")) {
            suggestions.add("Consider using parallel streams for better performance.");
        }

        // Add more checks as needed

        return suggestions;
    }
}