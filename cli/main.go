package main

import (
	"flag"
	"fmt"
	"time"

	"github.com/axentx/surrogate-1/internal/event"
)

func main() {
	eventName := flag.String("event", "", "Event name (e.g., user_login)")
	attributes := flag.String("attributes", "", "Event attributes (e.g., user_id=123)")
	timestamp := flag.Time("timestamp", time.Now(), "Event timestamp")
	numEvents := flag.Int("count", 1, "Number of events to generate")

	flag.Parse()

	if *eventName == "" {
		fmt.Println("Event name is required")
		return
	}

	for i := 0; i < *numEvents; i++ {
		e := event.Event{
			Name:        *eventName,
			Attributes:  event.ParseAttributes(*attributes),
			Timestamp:   *timestamp,
			SequenceNum: i + 1,
		}
		fmt.Printf("%s\n", e.ToJSON())
	}
}

// Summary:
// - Added CLI flags for event name, attributes, timestamp, and event count.
// - Implemented generation of multiple events with a given event name and attributes.
// - Events are exported as JSON.