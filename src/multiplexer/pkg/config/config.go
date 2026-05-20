package config

import (
	"github.com/axentx/surrogate-1/pkg/config"
)

// GetInternalUDP returns the internal UDP endpoint.
func GetInternalUDP() *net.UDPAddr {
	return config.GetInternalUDP()
}