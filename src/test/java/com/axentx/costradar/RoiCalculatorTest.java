import org.junit.Test;

public class RoiCalculatorTest {
    @Test
    public void testCalculateRoi() {
        RoiCalculator.Component component = new RoiCalculator.Component("GPU", 1000, 10);
        double roi = component.calculateRoi();
        assert roi == 0.01;
    }
}