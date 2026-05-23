package parser

import (
	"fmt"
	"log"
	"time"

	"github.com/axentx/surrogate-1/src/utils/metrics"
)

var memoryMetrics = metrics.NewMemoryMetrics()

func init() {
	go monitorMemoryUsage()
}

func monitorMemoryUsage() {
	for {
		memoryMetrics.UpdateRSS()
		currentRSS := memoryMetrics.GetRSS()
		log.Printf("Current RSS: %d bytes", currentRSS)
		time.Sleep(5 * time.Second)
	}
}

func ProcessDataStream(dataStream chan []byte) {
	for data := range dataStream {
		// Process data here
		fmt.Println("Processing data chunk:", len(data))
		memoryMetrics.UpdateRSS()
		currentRSS := memoryMetrics.GetRSS()
		if currentRSS > 500*1024*1024 {
			log.Printf("Warning: Memory usage exceeded 500MB (%d bytes)", currentRSS)
		}
	}
}