package com.axentx.surrogate.forecasting;

import java.util.List;
import org.apache.commons.math3.stat.regression.SimpleRegression;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;

public class ForecastingService {

    public ForecastResult forecast(List<Double> historicalData, int forecastPeriods) {
        SimpleRegression regression = new SimpleRegression();
        for (int i = 0; i < historicalData.size(); i++) {
            regression.addData(i, historicalData.get(i));
        }

        ForecastResult result = new ForecastResult();
        result.setSlope(regression.getSlope());
        result.setIntercept(regression.getIntercept());

        DescriptiveStatistics stats = new DescriptiveStatistics();
        for (double value : historicalData) {
            stats.addValue(value);
        }

        double mean = stats.getMean();
        double stdDev = stats.getStandardDeviation();

        for (int i = 1; i <= forecastPeriods; i++) {
            double forecastValue = regression.predict(i + historicalData.size());
            double lowerBound = forecastValue - 1.96 * stdDev;
            double upperBound = forecastValue + 1.96 * stdDev;
            result.addForecast(new ForecastPoint(i, forecastValue, lowerBound, upperBound));
        }

        return result;
    }
}