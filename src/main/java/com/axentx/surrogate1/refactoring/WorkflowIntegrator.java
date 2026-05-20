package com.axentx.surrogate1.refactoring;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class WorkflowIntegrator {
    
    private final RefactoringEngine refactoringEngine;
    private final DeveloperWorkflow workflow;
    
    public WorkflowIntegrator(RefactoringEngine engine, DeveloperWorkflow workflow) {
        this.refactoringEngine = engine;
        this.workflow = workflow;
    }
    
    /**
     * Integrates automated refactoring suggestions into the developer workflow
     * @param codeIssues List of detected concurrency and performance issues
     * @return List of actionable refactoring suggestions
     */
    public List<RefactoringSuggestion> integrateSuggestions(List<CodeIssue> codeIssues) {
        List<RefactoringSuggestion> suggestions = new ArrayList<>();
        
        for (CodeIssue issue : codeIssues) {
            List<RefactoringSuggestion> issueSuggestions = refactoringEngine.generateSuggestions(issue);
            suggestions.addAll(issueSuggestions);
        }
        
        // Apply suggestions to workflow
        for (RefactoringSuggestion suggestion : suggestions) {
            workflow.addSuggestion(suggestion);
        }
        
        return suggestions;
    }
    
    /**
     * Applies a specific refactoring suggestion to the codebase
     * @param suggestion The refactoring suggestion to apply
     * @return true if successful, false otherwise
     */
    public boolean applySuggestion(RefactoringSuggestion suggestion) {
        try {
            // Validate suggestion before applying
            if (!suggestion.isValid()) {
                throw new IllegalArgumentException("Invalid refactoring suggestion");
            }
            
            // Apply the refactoring
            boolean success = workflow.applySuggestion(suggestion);
            
            if (success) {
                // Update the suggestion status
                suggestion.markAsApplied();
                workflow.updateSuggestionStatus(suggestion.getId(), "APPLIED");
            }
            
            return success;
        } catch (Exception e) {
            workflow.updateSuggestionStatus(suggestion.getId(), "FAILED");
            throw new RuntimeException("Failed to apply refactoring suggestion", e);
        }
    }
    
    /**
     * Gets all available suggestions for a given file
     * @param filePath The path to the file
     * @return List of suggestions for the file
     */
    public List<RefactoringSuggestion> getSuggestionsForFile(String filePath) {
        return workflow.getSuggestionsForFile(filePath);
    }
    
    /**
     * Gets summary of applied suggestions
     * @return Map containing statistics about applied suggestions
     */
    public Map<String, Object> getAppliedSuggestionsSummary() {
        Map<String, Object> summary = new HashMap<>();
        summary.put("totalApplied", workflow.getTotalApplied());
        summary.put("totalFailed", workflow.getTotalFailed());
        summary.put("successRate", workflow.getSuccessRate());
        return summary;
    }
}