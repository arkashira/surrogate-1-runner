public class InsightCalculationService {

    public static double calculateGrowth(double initialBalance, double currentBalance) {
        double growth = (currentBalance - initialBalance) / initialBalance * 100;
        return growth;
    }
}