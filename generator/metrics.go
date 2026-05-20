package generator

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"time"
)

// Metric represents a synthetic Datadog metric with time series data
type Metric struct {
	Name     string    `json:"metric"`
	Value    float64   `json:"value"`
	Timestamp time.Time `json:"timestamp"`
	Tags     map[string]string `json:"tags,omitempty"`
}

// TimeSeries represents a collection of metrics over time
type TimeSeries struct {
	Metrics []Metric `json:"metrics"`
}

// GenerateTimeSeries creates synthetic metrics at regular intervals
func GenerateTimeSeries(name string, values []float64, tags map[string]string, startTime time.Time, interval time.Duration) TimeSeries {
	var metrics []Metric
	
	for i, value := range values {
		timestamp := startTime.Add(time.Duration(i) * interval).UTC()
		metric := Metric{
			Name:     name,
			Value:    value,
			Timestamp: timestamp,
			Tags:     tags,
		}
		metrics = append(metrics, metric)
	}
	
	return TimeSeries{Metrics: metrics}
}

// ExportJSON converts time series to JSON format
func (ts TimeSeries) ExportJSON() ([]byte, error) {
	return json.MarshalIndent(ts, "", "  ")
}

// ExportCSV converts time series to CSV format
func (ts TimeSeries) ExportCSV() (string, error) {
	var csvData [][]string
	
	// Build header
	header := []string{"timestamp", "metric", "value"}
	for k := range ts.Metrics[0].Tags {
		header = append(header, k)
	}
	csvData = append(csvData, header)
	
	// Build rows
	for _, m := range ts.Metrics {
		row := []string{
			m.Timestamp.Format(time.RFC3339),
			m.Name,
			fmt.Sprintf("%f", m.Value),
		}
		
		// Add tags as columns
		for _, tagKey := range header[3:] {
			row = append(row, m.Tags[tagKey])
		}
		
		csvData = append(csvData, row)
	}
	
	return csvWriter(csvData)
}

func csvWriter(data [][]string) (string, error) {
	var b bytes.Buffer
	w := csv.NewWriter(&b)
	
	if err := w.WriteAll(data); err != nil {
		return "", err
	}
	
	w.Flush()
	return b.String(), nil
}