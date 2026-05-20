import org.apache.commons.math3.stat.descriptive.moment.Mean;
import org.apache.commons.math3.stat.descriptive.moment.StandardDeviation;
import org.apache.commons.math3.stat.descriptive.rank.Median;
import java.util.List;

public class AnomalyDetector {

    private static final double THRESHOLD = 2.0; // Adjust the threshold as needed

    public static boolean isAnomaly(double value, List<Double> historicalValues) {
        Mean mean = new Mean();
        StandardDeviation stdDev = new StandardDeviation();
        Median median = new Median();

        double meanValue = mean.evaluate(historicalValues);
        double stdDevValue = stdDev.evaluate(historicalValues);
        double medianValue = median.evaluate(historicalValues);

        double zScore = (value - meanValue) / stdDevValue;

        return Math.abs(zScore) > THRESHOLD || value < medianValue - THRESHOLD || value > medianValue + THRESHOLD;
    }
}