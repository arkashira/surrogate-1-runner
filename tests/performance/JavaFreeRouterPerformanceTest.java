import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class JavaFreeRouterPerformanceTest {

    @Test
    public void testPerformance() {
        // Create a test circuit
        Circuit circuit = new Circuit();
        circuit.addComponent(new Component());

        // Measure the time taken by the legacy FreeRouting
        long legacyTime = measureTime(() -> FreeRouting.route(circuit));

        // Measure the time taken by the new Java-free auto-router
        long newTime = measureTime(() -> JavaFreeRouter.route(circuit));

        // Assert that the new router is up to 2x faster
        assertTrue(newTime <= legacyTime / 2);
    }

    private long measureTime(Runnable task) {
        long startTime = System.currentTimeMillis();
        task.run();
        return System.currentTimeMillis() - startTime;
    }
}