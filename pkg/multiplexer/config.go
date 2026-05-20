package multiplexer

import (
	"fmt"
)

type Config struct {
	Rules []*Rule
}

func NewConfig(rules []*Rule) *Config {
	return &Config{
		Rules: rules,
	}
}

func (c *Config) Route(conn net.Conn) (string, error) {
	for _, rule := range c.Rules {
		if rule.Matches(conn) {
			return rule.Dest, nil
		}
	}

	return "", fmt.Errorf("no matching rule found")
}