package report

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/axentx/surrogate-1/internal/config"
	"github.com/axentx/surrogate-1/internal/repo"
)

type Report struct {
	RepoName     string    `json:"repo_name"`
	FilesFormatted int      `json:"files_formatted"`
	TotalTime    time.Duration `json:"total_time"`
}

func GenerateReport(repos map[string]*repo.Repo, startTime time.Time, endTime time.Time) (*Report, error) {
	report := &Report{
		RepoName:     "",
		FilesFormatted: 0,
		TotalTime: endTime.Sub(startTime),
	}

	for _, repo := range repos {
		report.RepoName = repo.Name
		report.FilesFormatted += len(repo.Files)
	}

	return report, nil
}

func PrintJSONReport(report *Report, logPath string) error {
	jsonReport, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		return err
	}

	if logPath != "" {
		logFile, err := os.Create(logPath)
		if err != nil {
			return err
		}
		defer logFile.Close()

		_, err = logFile.WriteString(string(jsonReport))
		if err != nil {
			return err
		}
	}

	fmt.Println(string(jsonReport))

	return nil
}