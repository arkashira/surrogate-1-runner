import org.junit.Test;
import static org.junit.Assert.*;

import java.util.List;

public class RecommendationGeneratorTest {

    @Test
    public void testGenerateRecommendations() {
        RecommendationGenerator generator = new RecommendationGenerator();
        List<String> recommendations = generator.generateRecommendations("HashMap");
        assertNotNull(recommendations);
        assertTrue(recommendations.size() > 0);
    }

    @Test
    public void testGenerateRecommendationsForConcurrentHashMap() {
        RecommendationGenerator generator = new RecommendationGenerator();
        List<String> recommendations = generator.generateRecommendations("ConcurrentHashMap");
        assertNotNull(recommendations);
        assertTrue(recommendations.size() > 0);
        assertTrue(recommendations.contains("java.util.concurrent.ConcurrentHashMap"));
    }
}