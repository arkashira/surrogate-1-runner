package com.axentx.surrogate.refactoring;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RefactoringSuggestionApplierTest {

    @Test
    public void testApplySuggestion() {
        RefactoringSuggestionApplier applier = new RefactoringSuggestionApplier();
        String testCode = "public class Test { synchronized void test() {} for (int i = 0; i < 10; i++) {} }";
        String suggestion = "Consider using concurrent collections instead of synchronized blocks.";
        String updatedCode = applier.applySuggestion(testCode, suggestion);

        assertTrue(updatedCode.contains("ConcurrentHashMap"));

        suggestion = "Consider using parallel streams for better performance.";
        updatedCode = applier.applySuggestion(testCode, suggestion);

        assertTrue(updatedCode.contains("IntStream.range(0, 10).parallel().forEach(i ->"));
    }
}