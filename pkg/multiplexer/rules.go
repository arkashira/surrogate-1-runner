package multiplexer

import (
	"net"
)

type Rule struct {
	Port     int
	Protocol string
	Dest     string
}

func NewRule(port int, protocol string, dest string) *Rule {
	return &Rule{
		Port:     port,
		Protocol: protocol,
		Dest:     dest,
	}
}

func (r *Rule) Matches(conn net.Conn) bool {
	if r.Protocol != conn.LocalAddr().Network() {
		return false
	}

	localAddr, ok := conn.LocalAddr().(*net.TCPAddr)
	if !ok {
		return false
	}

	return localAddr.Port == r.Port
}