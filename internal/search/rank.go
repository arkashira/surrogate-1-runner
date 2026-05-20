package search

import (
	"sort"
	"strings"
	"unicode"
)

// SearchResult represents a single search hit. It is assumed to be defined
// elsewhere in the project, but we include a minimal definition here to
// keep the file self‑contained for compilation purposes. If the real
// definition differs, this struct will be overridden by the actual one.
type SearchResult struct {
	Path    string   // Markdown file path
	Tags    []string // AI‑generated tags
	Content string   // Full file content
	Score   float64  // Relevance score (populated by RankResults)
}

// RankResults ranks the provided search results based on the query.
// The relevance score is derived from:
//   - tagScore: number of tags that contain any query token (weight 2)
//   - contentScore: number of query tokens that appear in the content (weight 1)
// The results are sorted in descending order of score.
func RankResults(query string, results []SearchResult) []SearchResult {
	if len(results) == 0 {
		return results
	}

	// Optimize tokenization by reusing the tokenize function
	tokens := tokenize(query)

	for i, r := range results {
		tagScore := 0
		for _, tag := range r.Tags {
			if containsAny(tokenize(tag), tokens) {
				tagScore++
			}
		}

		contentScore := 0
		contentTokens := tokenize(r.Content)
		for _, t := range tokens {
			if contains(contentTokens, t) {
				contentScore++
			}
		}

		// Weighted sum: tags are twice as important as content matches.
		results[i].Score = float64(tagScore*2 + contentScore)
	}

	// Use a stable sort to preserve the original order of equal elements
	sort.SliceStable(results, func(i, j int) bool {
		return results[i].Score > results[j].Score
	})

	return results
}

// tokenize splits a string into lowercase alphanumeric tokens.
func tokenize(s string) []string {
	f := func(r rune) bool {
		return !unicode.IsLetter(r) && !unicode.IsDigit(r)
	}
	fields := strings.FieldsFunc(s, f)
	for i, f := range fields {
		fields[i] = strings.ToLower(f)
	}
	return fields
}

// contains reports whether slice contains the target string.
func contains(slice []string, target string) bool {
	for _, s := range slice {
		if s == target {
			return true
		}
	}
	return false
}

// containsAny reports whether any of the tokens in slice2 appear in slice1.
func containsAny(slice1, slice2 []string) bool {
	for _, t := range slice2 {
		if contains(slice1, t) {
			return true
		}
	}
	return false
}