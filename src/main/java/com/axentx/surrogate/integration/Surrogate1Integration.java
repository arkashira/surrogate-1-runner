package com.axentx.surrogate.integration;

import com.axentx.surrogate.refactor.ConcurrencyRefactorer;
import com.axentx.surrogate.refactor.RefactoringSuggestion;
import com.axentx.surrogate.model.ConcurrencyIssue;
import com.axentx.surrogate.model.CodeFile;

import java.util.List;

public class Surrogate1Integration {
    
    private final ConcurrencyRefactorer refactorer;
    
    public Surrogate1Integration() {
        this.refactorer = new ConcurrencyRefactorer();
    }
    
    /**
     * Provides automated refactoring suggestions for detected concurrency issues
     * @param issue The detected concurrency issue
     * @param file The code file containing the issue
     * @return List of refactoring suggestions
     */
    public List<RefactoringSuggestion> getRefactoringSuggestions(ConcurrencyIssue issue, CodeFile file) {
        return refactorer.generateSuggestions(issue, file);
    }
    
    /**
     * Integrates with the surrogate-1 project by processing concurrency issues
     * @param issues List of detected concurrency issues
     * @param file The code file being analyzed
     * @return Processed refactoring recommendations
     */
    public List<RefactoringSuggestion> processConcurrencyIssues(List<ConcurrencyIssue> issues, CodeFile file) {
        return issues.stream()
                .map(issue -> getRefactoringSuggestions(issue, file))
                .flatMap(List::stream)
                .toList();
    }
}