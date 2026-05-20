package multiplexer

import (
	"net"
	"errors"
)

// DatagramHandler interface for handling datagrams
type DatagramHandler interface {
	HandleDatagram(conn net.PacketConn, buf []byte) error
}

// NewDatagramHandler creates a new datagram handler based on protocol
func NewDatagramHandler(protocol string) (DatagramHandler, error) {
	switch protocol {
	case "udp":
		return NewUDPHandler(), nil
	case "tcp":
		return NewTCPHandler(), nil
	// Add other protocols as needed
	default:
		return nil, errors.New("unsupported protocol")
	}
}