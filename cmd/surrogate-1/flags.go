package main

import (
	"strings"

	"github.com/spf13/pflag"
)

// ParseReposFlag parses a slice of CLI arguments and extracts the value of the
// `--repos` flag, returning a slice of repository paths. The flag accepts a
// comma‑separated list (e.g. "--repos=repo1,repo2").
// If the flag is omitted, an empty slice is returned.
// Errors from flag parsing are propagated to the caller.
func ParseReposFlag(args []string) ([]string, error) {
	fs := pflag.NewFlagSet("surrogate-1-test", pflag.ContinueOnError)
	var repos string
	fs.StringVar(&repos, "repos", "", "comma‑separated list of repository paths")
	if err := fs.Parse(args); err != nil {
		return nil, err
	}
	if repos == "" {
		return []string{}, nil
	}
	parts := strings.Split(repos, ",")
	for i, p := range parts {
		parts[i] = strings.TrimSpace(p)
	}
	return parts, nil
}