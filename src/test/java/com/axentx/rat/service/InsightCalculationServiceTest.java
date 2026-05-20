import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class InsightCalculationServiceTest {

    @Test
    public void testGrowthCalculation() {
        // Arrange
        double initialBalance = 100.0;
        double currentBalance = 120.0;
        double expectedGrowth = 20.0;

        // Act
        double growth = InsightCalculationService.calculateGrowth(initialBalance, currentBalance);

        // Assert
        assertEquals(expectedGrowth, growth, 0.01);
    }

    @Test
    public void testNoGrowth() {
        // Arrange
        double initialBalance = 100.0;
        double currentBalance = 100.0;
        double expectedGrowth = 0.0;

        // Act
        double growth = InsightCalculationService.calculateGrowth(initialBalance, currentBalance);

        // Assert
        assertEquals(expectedGrowth, growth, 0.01);
    }

    @Test
    public void testNegativeGrowth() {
        // Arrange
        double initialBalance = 100.0;
        double currentBalance = 80.0;
        double expectedGrowth = -20.0;

        // Act
        double growth = InsightCalculationService.calculateGrowth(initialBalance, currentBalance);

        // Assert
        assertEquals(expectedGrowth, growth, 0.01);
    }
}