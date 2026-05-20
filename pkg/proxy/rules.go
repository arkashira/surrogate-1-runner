package proxy

import (
	"net"
)

type Rule interface {
	Matches(conn net.Conn) bool
	Handle(conn net.Conn)
}

type ProtocolRule struct {
	Protocol string
	Port     int
	Handler  func(net.Conn)
}

func (pr *ProtocolRule) Matches(conn net.Conn) bool {
	tcpConn, ok := conn.(*net.TCPConn)
	if !ok {
		return false
	}

	localAddr := tcpConn.LocalAddr().(*net.TCPAddr)
	return localAddr.Port == pr.Port && localAddr.Network() == pr.Protocol
}

func (pr *ProtocolRule) Handle(conn net.Conn) {
	pr.Handler(conn)
}