package notifications

type Config struct {
	ErrorNotifications map[string]NotificationConfig `yaml:"error_notifications"`
}

type NotificationConfig struct {
	Enabled bool   `yaml:"enabled"`
	Recipients []string `yaml:"recipients"`
}

func NewConfig() *Config {
	return &Config{
		ErrorNotifications: make(map[string]NotificationConfig),
	}
}