package services

import (
	"bytes"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"net/http"
	"text/template"
	"time"
)

type NotifierConfig struct {
	Email struct {
		Enabled   bool   `yaml:"enabled"`
		From      string `yaml:"from"`
		ApiKey    string `yaml:"api_key"`
		SmtpHost  string `yaml:"smtp_host"`
		SlackWebhook string `yaml:"slack_webhook"`
	}

func LoadNotifierConfig() (NotifierConfig, error) {
	var config NotifierConfig
	data, err := ioutil.ReadFile("/opt/axentx/surrogate-1/config/notifiers.yaml")
	if err != nil {
		return config, err
	}
	err = yaml.Unmarshal(data, &config)
	return config, err
}

func SendSpendAlert(subject string, message string, threshold float64, current float64) error {
	config, err := LoadNotifierConfig()
	if err != nil {
		return err
	}

	if config.Email.Enabled {
		// Email implementation would go here
		// Using SendGrid or similar SMTP service
	}

	if config.Slack.Enabled {
		// Slack implementation
		slackMsg := map[string]interface{}{
			"text":        message,
			"attachments": []map[string]string{
				{
					"fallback": "Spend alert details",
					"color":    "danger",
					"fields": []map[string]string{
						{"title": "Threshold", "value": "$" + formatCurrency(threshold), "short": true},
						{"title": "Current", "value": "$" + formatCurrency(current), "short": true},
					},
					"footer": "Spend Alert - " + time.Now().Format(time.RFC3339),
				},
			},
		}

		jsonData, _ := json.Marshal(slackMsg)
		resp, err := http.Post(config.Slack.Webhook, "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			return err
		}
		resp.Body.Close()
	}

	return nil
}

func formatCurrency(amount float64) string {
	return strconv.FormatFloat(amount, 'f', 2, 64)
}