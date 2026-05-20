package multiplexer

import (
	"fmt"
	"net"
	"sync"

	"github.com/axentx/surrogate-1/pkg/config"
	"github.com/axentx/surrogate-1/pkg/metrics"
)

// UDPListener represents a UDP listener.
type UDPListener struct {
	listener    net.PacketConn
	internalUDP *net.UDPAddr
	mu          sync.Mutex
}

// NewUDPListener creates a new UDP listener.
func NewUDPListener(port int) (*UDPListener, error) {
	listener, err := net.ListenUDP("udp", &net.UDPAddr{Port: port})
	if err != nil {
		return nil, err
	}
	return &UDPListener{
		listener:    listener,
		internalUDP: config.GetInternalUDP(),
	}, nil
}

// ForwardPacket forwards a UDP packet to the internal UDP endpoint.
func (l *UDPListener) ForwardPacket(packet []byte) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.internalUDP == nil {
		metrics.IncrementNoMappingCounter()
		return nil
	}
	_, err := l.listener.WriteTo(packet, l.internalUDP)
	return err
}

// Start starts the UDP listener.
func (l *UDPListener) Start() {
	go func() {
		for {
			buf := make([]byte, 1024)
			n, addr, err := l.listener.ReadFrom(buf)
			if err != nil {
				fmt.Println(err)
				continue
			}
			packet := buf[:n]
			l.ForwardPacket(packet)
		}
	}()
}

// Close closes the UDP listener.
func (l *UDPListener) Close() error {
	return l.listener.Close()
}