package detector

import (
	"encoding/json"
	"fmt"
	"os"
)

// impl is the singleton that satisfies the internal detector contract.
var impl detectorImpl = fileBasedDetector{}

// detectorImpl defines the minimal behaviour we need.
type detectorImpl interface {
	Detect() ([]DriftEvent, error)
}

/* ----------------------------------------------------------------------
   1️⃣  File‑based stub – works out‑of‑the‑box for CI
   ---------------------------------------------------------------------- */
type fileBasedDetector struct{}

// Detect reads a JSON file called “drift_events.json” from the current
// working directory.  If the file does not exist we treat it as “no drift”.
func (f fileBasedDetector) Detect() ([]DriftEvent, error) {
	const fileName = "drift_events.json"

	data, err := os.ReadFile(fileName)
	if err != nil {
		if os.IsNotExist(err) {
			// No file → no drift.
			return []DriftEvent{}, nil
		}
		return nil, fmt.Errorf("reading %s: %w", fileName, err)
	}

	var events []DriftEvent
	if err := json.Unmarshal(data, &events); err != nil {
		return nil, fmt.Errorf("parsing %s: %w", fileName, err)
	}
	return events, nil
}

/* ----------------------------------------------------------------------
   2️⃣  Hook for a future “real” detector
   ---------------------------------------------------------------------- */
// The following type shows how a richer detector could be added without
// touching the CLI.  It is **not used right now** – the file‑based stub
// remains the default – but the code is kept as a reference and can be
// swapped in by re‑assigning the `impl` variable in an init() function
// or via a build‑tag.
//
// type realDetector struct {
//     // fields such as AWS SDK clients, config, etc.
// }
//
// func (r realDetector) Detect() ([]DriftEvent, error) {
//     // …real detection logic…
//     return []DriftEvent{{Message: "example real drift"}}, nil
// }