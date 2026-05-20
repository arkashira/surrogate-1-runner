package cli

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var (
	metricConfigFile string
	dryRun           bool
)

func init() {
	generateCmd.Flags().StringVarP(&metricConfigFile, "config", "c", "", "path to the metric configuration file")
	generateCmd.Flags().BoolVarP(&dryRun, "dry-run", "d", false, "validate the config and print the would-be payload without sending")
}

var generateCmd = &cobra.Command{
	Use:   "generate",
	Short: "Generate synthetic metrics locally",
	Long:  `Generate synthetic metrics locally and stream them to a mock endpoint.`,
	Run: func(cmd *cobra.Command, args []string) {
		if metricConfigFile == "" {
			log.Fatal("config file is required")
		}

		config, err := loadMetricConfig(metricConfigFile)
		if err != nil {
			log.Fatalf("failed to load metric config: %v", err)
		}

		if dryRun {
			payload, err := json.Marshal(config.Payload)
			if err != nil {
				log.Fatalf("failed to marshal payload: %v", err)
			}
			fmt.Println(string(payload))
			return
		}

		streamer := sdk.NewStreamer("http://localhost:8125")
		err = streamer.Stream(config.Payload)
		if err != nil {
			log.Fatalf("failed to stream data: %v", err)
		}

		fmt.Println("Data streamed successfully")
	},
}

func loadMetricConfig(file string) (*MetricConfig, error) {
	data, err := os.ReadFile(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var config MetricConfig
	err = json.Unmarshal(data, &config)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal config: %w", err)
	}

	return &config, nil
}

type MetricConfig struct {
	Payload interface{} `json:"payload"`
}

func setupLogger() *zap.Logger {
	config := zap.NewProductionConfig()
	config.OutputPaths = []string{"stdout"}
	config.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
	logger, err := config.Build()
	if err != nil {
		log.Fatalf("failed to initialize logger: %v", err)
	}
	return logger
}