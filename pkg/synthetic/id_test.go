//go:build test
package synthetic

func generateEventID() string { return NewDeterministicID() }