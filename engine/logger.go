package engine

import (
	"log"
)

// Logger represents a logger
type Logger struct {
	logger *log.Logger
}

// NewLogger returns a new logger
func NewLogger() *Logger {
	return &Logger{
		logger: log.New(log.Writer(), "workflow-execution-engine: ", log.Ldate|log.Ltime|log.Lshortfile),
	}
}

// Printf prints a formatted message
func (l *Logger) Printf(format string, v ...interface{}) {
	l.logger.Printf(format, v...)
}