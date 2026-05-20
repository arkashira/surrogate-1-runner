
package compliance

import (
	"regexp"
	"strings"
)

var PIIRegexes = map[string][]*regexp.Regexp{
	"US": {
		regexp.MustCompile(`\bSSN\d{3}-?\d{2}-?\d{4}\b`),
		regexp.MustCompile(`\bEmail: ([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b`),
		// Add more US PII patterns as needed
	},
	// Add more countries and their PII patterns as needed
}

func IsPII(text string, country string) bool {
	re, ok := PIIRegexes[country]
	if !ok {
		return false
	}
	for _, r := range re {
		if r.MatchString(text) {
			return true
		}
	}
	return false
}