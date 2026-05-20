package com.axentx.surrogate1;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.concurrent.ConcurrentHashMap;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PerformanceAnalyzerTest {

    private final PerformanceAnalyzer analyzer = new PerformanceAnalyzer();

    @Test
    public void testAnalyzeCollectionPerformance() {
        Collection<?> collection = new ConcurrentHashMap<>();
        analyzer.analyzeCollectionPerformance(collection);
        // Verify the warning output (mocking or capturing output can be done here)
    }

    @Test
    public void testAnalyzeIteratorUsage() {
        Iterator<?> iterator = Arrays.asList(1, 2, 3).iterator();
        analyzer.analyzeIteratorUsage(iterator);
        // Verify the behavior when iterator is used correctly
    }

    @Test
    public void testSuggestAlternativeDataStructure() {
        Collection<?> collection = new ConcurrentHashMap<>();
        String suggestion = analyzer.suggestAlternativeDataStructure(collection);
        assertEquals("Consider using a non-synchronized collection like ArrayList or HashMap for better performance.", suggestion);
    }
}