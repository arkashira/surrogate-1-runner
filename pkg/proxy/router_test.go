package proxy

import (
	"net"
	"testing"
)

func TestRouter(t *testing.T) {
	r := NewRouter([]Rule{})

	tcpRule := &ProtocolRule{
		Protocol: "tcp",
		Port:     8080,
		Handler:  func(conn net.Conn) {},
	}
	r.AddRule(tcpRule)

	conn := &net.TCPConn{}
	conn.LocalAddr = &net.TCPAddr{Port: 8080, Network: "tcp"}

	r.Route(conn)
}