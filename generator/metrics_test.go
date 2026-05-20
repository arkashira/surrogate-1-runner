package generator

import (
	"testing"
	"time"
)

func TestTimeSeriesGeneration(t *testing.T) {
	tags := map[string]string{
		"env": "dev",
		"region": "us-west",
	}
	
	startTime := time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	values := []float64{70.5, 72.3, 68.9}
	interval := time.Minute
	
	ts := GenerateTimeSeries("cpu_usage", values, tags, startTime, interval)
	
	if len(ts.Metrics) != 3 {
		t.Errorf("Expected 3 metrics, got %d", len(ts.Metrics))
	}
	
	for i, m := range ts.Metrics {
		expectedTime := startTime.Add(time.Duration(i) * interval)
		if !m.Timestamp.Equal(expectedTime) {
			t.Errorf("Timestamp mismatch at index %d: expected %v, got %v", i, expectedTime, m.Timestamp)
		}
		
		if m.Value != values[i] {
			t.Errorf("Value mismatch at index %d: expected %f, got %f", i, values[i], m.Value)
		}
		
		if len(m.Tags) != 2 {
			t.Errorf("Tags count mismatch at index %d: expected 2, got %d", i, len(m.Tags))
		}
	}
}