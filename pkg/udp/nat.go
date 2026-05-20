package udp

import (
	"net"
	"time"
)

type NAT struct {
	mappings map[int]string
	metrics  *Metrics
}

type Metrics struct {
	PacketsDropped uint64
}

func NewNAT(config []UDPMapping) *NAT {
	m := make(map[int]string)
	for _, mapping := range config {
		port, _ := strconv.Atoi(mapping.PublicPort)
		m[port] = mapping.InternalEndpoint
	}
	return &NAT{
		mappings: m,
		metrics:  &Metrics{},
	}
}

func (n *NAT) HandlePacket(conn *net.UDPConn, packet []byte, addr net.Addr) {
	port, _ := strconv.Atoi(addr.(*net.UDPAddr).Port)
	if internalEndpoint, exists := n.mappings[port]; exists {
		internalAddr, err := net.ResolveUDPAddr("udp", internalEndpoint)
		if err != nil {
			n.metrics.PacketsDropped++
			return
		}
		_, err = conn.WriteToUDP(packet, internalAddr)
		if err != nil {
			n.metrics.PacketsDropped++
		}
	} else {
		n.metrics.PacketsDropped++
	}
}

func (n *NAT) HandleNATTraversal(conn *net.UDPConn, packet []byte, addr net.Addr) {
	// Implement NAT hole-punching logic here
}