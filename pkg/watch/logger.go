package watch

import (
	"log"
)

// Logger represents a logger.
type Logger interface {
	Println(v ...interface{})
}

// NewLogger returns a new logger instance.
func NewLogger() Logger {
	return log.New(log.Writer(), "", log.LstdFlags)
}