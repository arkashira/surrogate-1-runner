package agent

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/natefinch/lumberjack"
)

const (
	defaultLogRotateDaily = true
	defaultLogRotateSize  = 100 * 1024 * 1024 // 100MB
	defaultLogRotateCount  = 30
)

type loggingConfig struct {
	rotateDaily bool
	rotateSize  int
	rotateCount int
}

func (c loggingConfig) getLogRotateConfig() lumberjack.Logger {
	return lumberjack.Logger{
		Filename:   filepath.Join(os.Getenv("PROGRAMDATA"), "Surrogate", "agent.log"),
		MaxSize:    c.rotateSize,
		MaxBackups: c.rotateCount,
		MaxAge:     28, // 4 weeks
		Compress:   false,
		LocalTime:  true,
	}
}

func (c loggingConfig) getLogRotateFunc() func() {
	if c.rotateDaily {
		return func() {
			log.Println("Rotating log file daily...")
			if err := os.Rename(filepath.Join(os.Getenv("PROGRAMDATA"), "Surrogate", "agent.log"), filepath.Join(os.Getenv("PROGRAMDATA"), "Surrogate", "agent.log.1")); err != nil {
				log.Printf("Error rotating log file: %v", err)
			}
		}
	}
	return func() {}
}

func (c loggingConfig) getLogFunc() func(string, ...interface{}) {
	return func(format string, a ...interface{}) {
		log.Printf(format, a...)
	}
}

func (c loggingConfig) getLogFuncErr() func(error) {
	return func(err error) {
		if err != nil {
			log.Printf("Error: %v", err)
		}
	}
}

func NewLoggingConfig() loggingConfig {
	return loggingConfig{
		rotateDaily: defaultLogRotateDaily,
		rotateSize:  defaultLogRotateSize,
		rotateCount: defaultLogRotateCount,
	}
}

func init() {
	log.SetFlags(0)
	log.SetOutput(&log.Logger{Out: os.Stdout, Flags: log.Ldate | log.Ltime | log.Lshortfile})
}