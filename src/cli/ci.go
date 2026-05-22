package cli

import (
	"fmt"
	"os"

	"github.com/axentx/surrogate-1/src/detector"
	"github.com/spf13/cobra"
)

// NewCICmd returns a cobra command that runs drift detection in CI.
// It prints a markdown‑friendly summary and exits:
//   0 – no drift
//   1 – drift detected (non‑zero so CI can fail)
//   >1 – unexpected error
func NewCICmd() *cobra.Command {
	return &cobra.Command{
		Use:   "ci",
		Short: "Run drift detection and fail the job if drift is present",
		Run: func(cmd *cobra.Command, args []string) {
			events, err := detector.Detect()
			if err != nil {
				// Unexpected error → exit code 2
				fmt.Fprintf(os.Stderr, "error running detector: %v\n", err)
				os.Exit(2)
			}

			if len(events) > 0 {
				// Markdown output works nicely with GitHub Actions `::error` or comment steps.
				fmt.Fprintln(os.Stdout, "## :warning: Drift detected")
				for _, e := range events {
					fmt.Fprintf(os.Stdout, "- %s\n", e.Message)
				}
				// In a real GitHub Action you could now call the GitHub API to post a comment.
				os.Exit(1)
			}

			fmt.Fprintln(os.Stdout, "✅ No drift detected.")
			os.Exit(0)
		},
	}
}