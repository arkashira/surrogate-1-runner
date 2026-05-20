package utils

import (
	"net"
	"strings"
)

// MaskIP masks the last octet of an IPv4 address for compliance.
// If the input is not a valid IPv4 address it is returned unchanged.
func MaskIP(ip string) string {
	parsed := net.ParseIP(ip)
	if parsed == nil || parsed.To4() == nil {
		return ip
	}
	parts := strings.Split(ip, ".")
	parts[3] = "XXX"
	return strings.Join(parts, ".")
}