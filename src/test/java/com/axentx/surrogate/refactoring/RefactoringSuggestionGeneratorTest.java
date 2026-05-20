package com.axentx.surrogate.refactoring;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

public class RefactoringSuggestionGeneratorTest {

    @Test
    public void testGenerateSuggestions() {
        RefactoringSuggestionGenerator generator = new RefactoringSuggestionGenerator();
        String testCode = "public class Test { synchronized void test() {} for (int i = 0; i < 10; i++) {} }";
        List<String> suggestions = generator.generateSuggestions(testCode);

        assertTrue(suggestions.contains("Consider using concurrent collections instead of synchronized blocks."));
        assertTrue(suggestions.contains("Consider using parallel streams for better performance."));
    }
}