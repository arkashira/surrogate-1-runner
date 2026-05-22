package meshing

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"strconv"
	"testing"
)

// ---------------------------------------------------------------------
// CSV utilities
// ---------------------------------------------------------------------

// loadCSV reads a CSV file into a slice of float64 slices.
// It automatically skips a single header row if the first row contains
// any non‑numeric field.
func loadCSV(path string) ([][]float64, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("open %s: %w", path, err)
	}
	defer f.Close()

	r := csv.NewReader(f)
	records, err := r.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("read %s: %w", path, err)
	}
	if len(records) == 0 {
		return nil, nil // empty file → empty matrix
	}

	// Detect a header row: if any field cannot be parsed as float,
	// treat the whole first row as a header and skip it.
	start := 0
	if _, err := strconv.ParseFloat(records[0][0], 64); err != nil {
		start = 1
	}

	data := make([][]float64, 0, len(records)-start)
	for _, rec := range records[start:] {
		row := make([]float64, len(rec))
		for i, s := range rec {
			val, err := strconv.ParseFloat(s, 64)
			if err != nil {
				return nil, fmt.Errorf("parse %s:%d:%d (%q): %w", path, len(data), i, s, err)
			}
			row[i] = val
		}
		data = append(data, row)
	}
	return data, nil
}

// ---------------------------------------------------------------------
// Comparison utilities
// ---------------------------------------------------------------------

// tolerance is the maximum relative difference allowed (1 %).
const tolerance = 0.01

// compareWithinTolerance aborts the test if a and b differ by more than
// `tolerance`.  It also checks that the matrices have identical shape.
func compareWithinTolerance(t *testing.T, a, b [][]float64) {
	if len(a) != len(b) {
		t.Fatalf("row count mismatch: got %d, want %d", len(a), len(b))
	}
	for i := range a {
		if len(a[i]) != len(b[i]) {
			t.Fatalf("column count mismatch at row %d: got %d, want %d", i, len(a[i]), len(b[i]))
		}
		for j := range a[i] {
			av, bv := a[i][j], b[i][j]

			// If both are exactly zero we consider them equal.
			if av == 0 && bv == 0 {
				continue
			}
			relDiff := math.Abs(av-bv) / math.Max(math.Abs(av), math.Abs(bv))
			if relDiff > tolerance {
				t.Fatalf(
					"value mismatch at (%d,%d): got %g, want %g (diff %.2f %%)",
					i, j, av, bv, relDiff*100,
				)
			}
		}
	}
}

// ---------------------------------------------------------------------
// The actual integration test
// ---------------------------------------------------------------------

func TestGroupingAgainstLegacy(t *testing.T) {
	// -----------------------------------------------------------------
	// 1️⃣  Locate test fixtures (relative to repository root)
	// -----------------------------------------------------------------
	fixtureDir := filepath.Join("testdata", "grouping")
	inputPath := filepath.Join(fixtureDir, "input.csv")
	legacyPath := filepath.Join(fixtureDir, "legacy_output.csv")

	// -----------------------------------------------------------------
	// 2️⃣  Run the new implementation.
	// -----------------------------------------------------------------
	// We write the result to a temporary file so the repository stays
	// pristine even when the test is run in parallel.
	tmpDir := t.TempDir()
	gotPath := filepath.Join(tmpDir, "got_output.csv")

	// `GroupData` is the public entry point that the production code
	// should expose.  If only `Group([][]float64)` exists, add a thin
	// wrapper in the package:
	//
	//   func GroupData(in, out string) error {
	//       data, err := loadCSV(in)
	//       if err != nil { return err }
	//       grouped, err := Group(data)
	//       if err != nil { return err }
	//       return writeCSV(out, grouped)
	//   }
	//
	if err := GroupData(inputPath, gotPath); err != nil {
		t.Fatalf("GroupData failed: %v", err)
	}

	// -----------------------------------------------------------------
	// 3️⃣  Load both CSVs.
	// -----------------------------------------------------------------
	got, err := loadCSV(gotPath)
	if err != nil {
		t.Fatalf("load generated CSV: %v", err)
	}
	legacy, err := loadCSV(legacyPath)
	if err != nil {
		t.Fatalf("load legacy CSV: %v", err)
	}

	// -----------------------------------------------------------------
	// 4️⃣  Compare with the 1 % tolerance.
	// -----------------------------------------------------------------
	compareWithinTolerance(t, got, legacy)
}