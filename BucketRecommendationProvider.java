package com.example.cloudopt;

import java.util.List;

public final class BucketRecommendationProvider implements RecommendationProvider<StorageBucket> {

    @Override
    public List<Recommendation> recommend(StorageBucket bucket) {
        if (bucket.getLastAccessedHoursAgo() > 720) {   // >30 days
            return List.of(
                new Recommendation(
                    "Archive bucket " + bucket.getId(),
                    "Last accessed " + bucket.getLastAccessedHoursAgo() + " hours ago",
                    bucket::archive
                )
            );
        }
        return List.of();
    }
}