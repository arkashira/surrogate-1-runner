package com.axentx.surrogate.refactoring;

public class RefactoringSuggestionApplier {

    public String applySuggestion(String code, String suggestion) {
        // Apply the suggestion to the code
        if (suggestion.equals("Consider using concurrent collections instead of synchronized blocks.")) {
            code = code.replace("synchronized", "ConcurrentHashMap");
        } else if (suggestion.equals("Consider using parallel streams for better performance.")) {
            code = code.replace("for (int i = 0; i < ", "IntStream.range(0, ").replace("; i++)", ").parallel().forEach(i ->");
        }

        // Add more suggestions as needed

        return code;
    }
}