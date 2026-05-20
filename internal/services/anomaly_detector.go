package services

import (
	"context"
	"fmt"
	"math"
	"time"

	"github.com/axentx/surrogate-1/models"
)

// DataPoint holds a single measurement together with the time it was taken.
type DataPoint struct {
	Value     float64
	Timestamp time.Time
}

// AnomalyDetector keeps a sliding window of recent measurements and
// flags values that are more than `threshold` standard deviations away
// from the mean of that window.
type AnomalyDetector struct {
	threshold      float64
	lookbackPeriod time.Duration
	historicalData []DataPoint
}

// NewAnomalyDetector creates a detector that will keep data points for
// the last `lookbackPeriod` and will flag any value that is
// `threshold` standard deviations away from the mean.
func NewAnomalyDetector(threshold float64, lookbackPeriod time.Duration) *AnomalyDetector {
	return &AnomalyDetector{
		threshold:      threshold,
		lookbackPeriod: lookbackPeriod,
		historicalData: make([]DataPoint, 0),
	}
}

// AddDataPoint appends a new measurement and immediately removes any
// points that are older than the look‑back window.
func (ad *AnomalyDetector) AddDataPoint(value float64, timestamp time.Time) {
	ad.historicalData = append(ad.historicalData, DataPoint{Value: value, Timestamp: timestamp})
	ad.removeOldDataPoints(timestamp)
}

// removeOldDataPoints keeps only the points that are newer than
// `currentTime - lookbackPeriod`.  It runs in O(n) but the slice is
// usually tiny (a few dozen points), so the cost is negligible.
func (ad *AnomalyDetector) removeOldDataPoints(currentTime time.Time) {
	cutoff := currentTime.Add(-ad.lookbackPeriod)
	i := 0
	for _, dp := range ad.historicalData {
		if dp.Timestamp.After(cutoff) {
			break
		}
		i++
	}
	ad.historicalData = ad.historicalData[i:]
}

// DetectAnomaly returns true if the supplied value is more than
// `threshold` standard deviations away from the mean of the current
// window.  If the window is empty, false is returned.
func (ad *AnomalyDetector) DetectAnomaly(currentValue float64) bool {
	if len(ad.historicalData) == 0 {
		return false
	}
	mean := ad.calculateMean()
	stdDev := ad.calculateStdDev(mean)

	// Guard against a zero stdDev – in that case we consider the
	// value normal (no variation in the window).
	if stdDev == 0 {
		return false
	}

	z := math.Abs((currentValue - mean) / stdDev)
	return z > ad.threshold
}

// calculateMean computes the arithmetic mean of the current window.
func (ad *AnomalyDetector) calculateMean() float64 {
	sum := 0.0
	for _, dp := range ad.historicalData {
		sum += dp.Value
	}
	return sum / float64(len(ad.historicalData))
}

// calculateStdDev returns the *standard* deviation of the current window.
func (ad *AnomalyDetector) calculateStdDev(mean float64) float64 {
	sum := 0.0
	for _, dp := range ad.historicalData {
		diff := dp.Value - mean
		sum += diff * diff
	}
	variance := sum / float64(len(ad.historicalData))
	return math.Sqrt(variance)
}

// SendAlert is a placeholder that prints the alert.  Replace it with
// real email/Slack/DB logic as needed.
func (ad *AnomalyDetector) SendAlert(ctx context.Context, alert models.Alert) error {
	fmt.Printf("Sending alert: %+v\n", alert)
	return nil
}

// TrackAlertHistory is a placeholder that prints the history entry.
// Replace with persistence logic if required.
func (ad *AnomalyDetector) TrackAlertHistory(ctx context.Context, alert models.Alert) error {
	fmt.Printf("Tracking alert history: %+v\n", alert)
	return nil
}