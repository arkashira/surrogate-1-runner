package com.example.cloudopt;

/**
 * A pluggable provider that can generate recommendations for a specific
 * resource type.  The engine simply delegates to all registered providers.
 */
public interface RecommendationProvider<T extends CloudResource> {
    /** Return recommendations for the supplied resource, or an empty list. */
    List<Recommendation> recommend(T resource);
}