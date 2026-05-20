package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"github.com/axentx/surrogate-1/internal/config"
	"github.com/axentx/surrogate-1/internal/report"
	"github.com/axentx/surrogate-1/internal/repo"
)

func main() {
	flag.StringVar(&logPath, "log", "", "log file path")
	flag.StringVar(&reportPath, "report", "", "report file path")
	flag.Parse()

	startTime := time.Now()

	repos, err := repo.GetRepos()
	if err != nil {
		log.Fatal(err)
	}

	reportConfig, err := config.GetReportConfig()
	if err != nil {
		log.Fatal(err)
	}

	report, err := report.GenerateReport(repos, startTime, time.Now())
	if err != nil {
		log.Fatal(err)
	}

	if reportPath != "" {
		err = report.PrintJSONReport(report, reportPath)
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println("Report generated successfully")
}