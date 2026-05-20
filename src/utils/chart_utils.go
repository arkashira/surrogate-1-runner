package utils

import (
	"time"
	"math"
	"sort"
)

type ChartData struct {
	Timestamp time.Time `json:"timestamp"`
	Value     int64     `json:"value"`
	Anomaly   bool      `json:"anomaly,omitempty"`
}

type UsageTrend struct {
	Period    string     `json:"period"`
	ChartData []ChartData `json:"chart_data"`
	Average   float64    `json:"average"`
	MaxValue  int64      `json:"max_value"`
	Anomalies int        `json:"anomalies"`
}

func GetUsageTrends(rawData []map[string]interface{}, interval time.Duration) UsageTrend {
	if len(rawData) == 0 {
		return UsageTrend{Period: "none"}
	}

	// Sort by timestamp
	sort.Slice(rawData, func(i, j int) bool {
		ti := rawData[i]["timestamp"].(time.Time)
		tj := rawData[j]["timestamp"].(time.Time)
		return ti.Before(tj)
	})

	// Aggregate by time intervals
	aggregated := make([]ChartData, 0)
	currentBucket := time.Time{}
	currentSum := int64(0)
	currentCount := 0

	for _, item := range rawData {
		ts := item["timestamp"].(time.Time)
		value := item["value"].(int64)

		if currentBucket.IsZero() || ts.Sub(currentBucket) > interval {
			if currentCount > 0 {
				aggregated = append(aggregated, ChartData{
					Timestamp: currentBucket,
					Value:     currentSum / int64(currentCount),
				})
			}
			currentBucket = ts.Truncate(interval)
			currentSum = value
			currentCount = 1
		} else {
			currentSum += value
			currentCount++
		}
	}

	// Add final bucket
	if currentCount > 0 {
		aggregated = append(aggregated, ChartData{
			Timestamp: currentBucket,
			Value:     currentSum / int64(currentCount),
		})
	}

	// Calculate statistics
	values := make([]int64, len(aggregated))
	for i, data := range aggregated {
		values[i] = data.Value
	}

	average := calculateAverage(values)
	maxValue := values[0]
	for _, v := range values {
		if v > maxValue {
			maxValue = v
		}
	}

	// Detect anomalies using 3σ rule
	anomalyCount := 0
	for i := range aggregated {
		if i >= 7 && isAnomaly(values[i], values[i-7:i]) {
			aggregated[i].Anomaly = true
			anomalyCount++
		}
	}

	return UsageTrend{
		Period:    interval.String(),
		ChartData: aggregated,
		Average:   average,
		MaxValue:  maxValue,
		Anomalies: anomalyCount,
	}
}

func calculateAverage(values []int64) float64 {
	if len(values) == 0 {
		return 0
	}
	sum := int64(0)
	for _, v := range values {
		sum += v
	}
	return float64(sum) / float64(len(values))
}

func isAnomaly(current int64, history []int64) bool {
	if len(history) == 0 {
		return false
	}
	
	sum := int64(0)
	for _, v := range history {
		sum += v
	}
	avg := float64(sum) / float64(len(history))
	if avg == 0 {
		return false
	}
	
	deviation := math.Abs(float64(current) - avg)
	return deviation > 2.5*avg // 3σ rule approximation
}