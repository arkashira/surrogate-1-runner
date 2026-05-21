package com.axentx.surrogate1.analyzer;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ConcurrentCollectionAnalyzer {
    private static final Pattern COLLECTION_PATTERN = Pattern.compile(
        "(ArrayList|LinkedList|HashMap|TreeMap|HashSet|TreeSet)\\s+(\\w+)\\s*=\\s*new\\s+\\1\\s*\\("
    );

    public List<String> analyzeCollections(String code) {
        List<String> collectionUsages = new ArrayList<>();
        Matcher matcher = COLLECTION_PATTERN.matcher(code);

        while (matcher.find()) {
            String collectionType = matcher.group(1);
            String variableName = matcher.group(2);
            collectionUsages.add(collectionType + " " + variableName);
        }

        return collectionUsages;
    }
}