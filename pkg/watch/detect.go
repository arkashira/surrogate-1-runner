package watch

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/axentx/surrogate-1/pkg/event"
)

// MissedEventDetector detects and recovers from missed events.
type MissedEventDetector struct {
	eventStore event.Store
	resyncScope event.ResyncScope
	logger      *log.Logger
}

// NewMissedEventDetector returns a new MissedEventDetector instance.
func NewMissedEventDetector(eventStore event.Store, resyncScope event.ResyncScope, logger *log.Logger) *MissedEventDetector {
	return &MissedEventDetector{
		eventStore: eventStore,
		resyncScope: resyncScope,
		logger: logger,
	}
}

// DetectMissedEvents checks for missed events and triggers corrective resync if necessary.
func (d *MissedEventDetector) DetectMissedEvents(ctx context.Context) error {
	// Check for missed events
	missedEvents, err := d.eventStore.GetMissedEvents(ctx)
	if err != nil {
		return err
	}

	// Trigger corrective resync if missed events are found
	if len(missedEvents) > 0 {
		d.logger.Println("Missed events detected, triggering corrective resync...")
		if err := d.resyncScope.Resync(ctx); err != nil {
			return err
		}
		d.logger.Println("Corrective resync completed.")
	}

	return nil
}

func (d *MissedEventDetector) run(ctx context.Context) {
	ticker := time.NewTicker(30 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			if err := d.DetectMissedEvents(ctx); err != nil {
				d.logger.Println(err)
			}
		}
	}
}