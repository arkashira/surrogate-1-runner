import java.util.ArrayList;
import java.util.List;

public class RecommendationGenerator {
    private static final String[] EFFICIENT_COLLECTIONS = {
        "java.util.concurrent.ConcurrentHashMap",
        "java.util.concurrent.CopyOnWriteArrayList",
        "java.util.concurrent.ConcurrentLinkedQueue"
    };

    public List<String> generateRecommendations(String collectionType) {
        List<String> recommendations = new ArrayList<>();

        for (String efficientCollection : EFFICIENT_COLLECTIONS) {
            if (efficientCollection.contains(collectionType)) {
                recommendations.add(efficientCollection);
            }
        }

        return recommendations;
    }

    public static void main(String[] args) {
        RecommendationGenerator generator = new RecommendationGenerator();
        List<String> recommendations = generator.generateRecommendations("HashMap");
        System.out.println(recommendations);
    }
}