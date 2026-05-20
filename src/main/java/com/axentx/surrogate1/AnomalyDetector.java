import org.apache.commons.math3.stat.descriptive.moment.Mean;
import org.apache.commons.math3.stat.descriptive.moment.StandardDeviation;
import org.apache.commons.math3.stat.inference.TTest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class AnomalyDetector {
    private static final Logger logger = LoggerFactory.getLogger(AnomalyDetector.class);
    private static final double ALPHA = 0.01;

    public boolean isAnomaly(List<Double> expenses, List<Double> historicalMean, List<Double> historicalStdDev) {
        Mean mean = new Mean();
        StandardDeviation stdDev = new StandardDeviation();
        TTest tTest = new TTest();

        double currentMean = mean.evaluate(expenses);
        double currentStdDev = stdDev.evaluate(expenses);

        double tStat = tTest.tTest(historicalMean, historicalStdDev, currentMean, currentStdDev);
        double pValue = tTest.pValue(tStat, historicalMean.size());

        logger.debug("T-Statistic: {}, P-Value: {}", tStat, pValue);

        return pValue < ALPHA;
    }
}