package com.axentx.surrogate1;

import java.util.Collection;
import java.util.Iterator;
import java.util.concurrent.ConcurrentHashMap;

public class PerformanceAnalyzer {

    public void analyzeCollectionPerformance(Collection<?> collection) {
        if (collection instanceof ConcurrentHashMap) {
            System.out.println("Warning: Using ConcurrentHashMap may lead to excessive synchronization.");
        }
        // Additional checks for other collection types can be added here
    }

    public void analyzeIteratorUsage(Iterator<?> iterator) {
        if (iterator == null) {
            System.out.println("Warning: Iterator is null.");
            return;
        }
        // Example of improper usage detection
        if (!iterator.hasNext()) {
            System.out.println("Warning: Iterator has no elements to iterate.");
        }
    }

    public String suggestAlternativeDataStructure(Collection<?> collection) {
        if (collection instanceof ConcurrentHashMap) {
            return "Consider using a non-synchronized collection like ArrayList or HashMap for better performance.";
        }
        return "No alternative suggestions available.";
    }
}