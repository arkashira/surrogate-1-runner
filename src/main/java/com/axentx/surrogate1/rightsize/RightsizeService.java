package com.axentx.surrogate1.rightsize;

import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

@Service
public class RightsizeService {

    public List<Recommendation> getRecommendations() {
        List<Recommendation> recs = new ArrayList<>();

        // Example recommendation 1
        recs.add(new Recommendation(
                "vm-frontend-01",
                "t3.medium",
                "t3.large",
                0.12,
                0.24,
                15.0,
                55.0,
                0.12,
                43.0
        ));

        // Example recommendation 2
        recs.add(new Recommendation(
                "db-backend-02",
                "db.m5.large",
                "db.m5.xlarge",
                0.50,
                1.00,
                70.0,
                85.0,
                0.50,
                15.0
        ));

        return recs;
    }
}