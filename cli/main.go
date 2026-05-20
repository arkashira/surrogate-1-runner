package main

import (
	"flag"
	"fmt"
)

type Metric struct {
	Name  string
	Value float64
}

func main() {
	metricName := flag.String("metric-name", "", "Metric name")
	metricValue := flag.Float64("metric-value", 0, "Metric value")

	flag.Parse()

	if *metricName == "" {
		fmt.Println("Metric name is required")
		return
	}

	metric := Metric{
		Name:  *metricName,
		Value: *metricValue,
	}

	fmt.Printf("Generated metric: %+v\n", metric)
}