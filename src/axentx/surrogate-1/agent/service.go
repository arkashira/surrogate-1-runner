package agent

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/natefinch/lumberjack"
)

func (s *Service) run(ctx context.Context) {
	logConfig := NewLoggingConfig()
	logRotateFunc := logConfig.getLogRotateFunc()
	logFunc := logConfig.getLogFunc()
	logFuncErr := logConfig.getLogFuncErr()

	log.SetFlags(0)
	log.SetOutput(&log.Logger{Out: os.Stdout, Flags: log.Ldate | log.Ltime | log.Lshortfile})

	logRotate := func() {
		logRotateFunc()
		log.Println("Log rotation done.")
	}

	go func() {
		t := time.NewTicker(5 * time.Minute)
		defer t.Stop()
		for {
			select {
			case <-t.C:
				logRotate()
			case <-ctx.Done():
				return
			}
		}
	}()

	s.pollPolicyChanges(ctx)
}

func (s *Service) start() error {
	return s.run(context.Background())
}