package config

import (
	"errors"
	"fmt"
	"net"
	"time"
)

// ConfigVersion is the current schema version of the service mapping configuration
const ConfigVersion = "1.0.0"

// Config represents the root service mapping configuration
type Config struct {
	Version     string          `yaml:"version" json:"version"`
	UpdatedAt   time.Time       `yaml:"updated_at" json:"updated_at"`
	LoadTimeout time.Duration   `yaml:"load_timeout" json:"load_timeout"`
	Mappings    []ServiceMapping `yaml:"mappings" json:"mappings"`
}

// ServiceMapping defines a single service mapping rule
type ServiceMapping struct {
	ID            string            `yaml:"id" json:"id"`
	ExternalPort  int               `yaml:"external_port" json:"external_port"`
	Protocol      Protocol          `yaml:"protocol" json:"protocol"`
	InternalPorts []InternalPortRef `yaml:"internal_ports" json:"internal_ports"`
	Timeout       time.Duration     `yaml:"timeout" json:"timeout"`
	HealthCheck   *HealthCheck      `yaml:"health_check" json:"health_check"`
}

// InternalPortRef represents an internal service port reference
type InternalPortRef struct {
	ServiceName string `yaml:"service_name" json:"service_name"`
	Port        int    `yaml:"port" json:"port"`
}

// Protocol represents the network protocol
type Protocol string

const (
	ProtocolTCP Protocol = "tcp"
	ProtocolUDP Protocol = "udp"
)

// HealthCheck defines health check configuration
type HealthCheck struct {
	Interval time.Duration `yaml:"interval" json:"interval"`
	Timeout  time.Duration `yaml:"timeout" json:"timeout"`
}

// Validate validates the configuration structure
func (c *Config) Validate() error {
	if c.Version != ConfigVersion {
		return fmt.Errorf("invalid config version: expected %s, got %s", ConfigVersion, c.Version)
	}

	if len(c.Mappings) == 0 {
		return errors.New("at least one service mapping is required")
	}

	for i, m := range c.Mappings {
		if err := m.Validate(); err != nil {
			return fmt.Errorf("mapping[%d]: %w", i, err)
		}
	}

	return nil
}

// Validate validates a single service mapping
func (m *ServiceMapping) Validate() error {
	if m.ID == "" {
		return errors.New("mapping ID is required")
	}

	if m.ExternalPort <= 0 || m.ExternalPort > 65535 {
		return fmt.Errorf("external port must be between 1 and 65535, got %d", m.ExternalPort)
	}

	if m.Protocol != ProtocolTCP && m.Protocol != ProtocolUDP {
		return fmt.Errorf("protocol must be 'tcp' or 'udp', got '%s'", m.Protocol)
	}

	if len(m.InternalPorts) == 0 {
		return errors.New("at least one internal port mapping is required")
	}

	for i, ip := range m.InternalPorts {
		if ip.ServiceName == "" {
			return fmt.Errorf("internal port[%d]: service_name is required", i)
		}
		if ip.Port <= 0 || ip.Port > 65535 {
			return fmt.Errorf("internal port[%d]: port must be between 1 and 65535, got %d", i, ip.Port)
		}

		if _, err := net.LookupPort(m.Protocol, ip.Port); err != nil {
			return fmt.Errorf("internal port[%d]: invalid port for protocol %s: %w", i, m.Protocol, err)
		}
	}

	if m.Timeout <= 0 {
		return errors.New("timeout must be positive")
	}

	if m.HealthCheck != nil {
		if m.HealthCheck.Interval <= 0 {
			return errors.New("health_check.interval must be positive")
		}
		if m.HealthCheck.Timeout <= 0 {
			return errors.New("health_check.timeout must be positive")
		}
	}

	return nil
}

// GetProtocol returns the protocol string representation
func (p Protocol) String() string {
	return string(p)
}

// IsTCP returns true if the protocol is TCP
func (p Protocol) IsTCP() bool {
	return p == ProtocolTCP
}

// IsUDP returns true if the protocol is UDP
func (p Protocol) IsUDP() bool {
	return p == ProtocolUDP
}