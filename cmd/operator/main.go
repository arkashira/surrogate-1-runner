package main

import (
	"context"
	"fmt"
	"log"

	"github.com/axentx/axentx-go/internal/sdk"
)

func main() {
	// Create a new context
	ctx := context.Background()

	// Create a new options instance
	opts := &sdk.Options{}

	// Start the snapshot stream
	if err := sdk.StartSnapshotStream(ctx, opts); err != nil {
		log.Fatal(err)
	}

	fmt.Println("Snapshot stream started")
}