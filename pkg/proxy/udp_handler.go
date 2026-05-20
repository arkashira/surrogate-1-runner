package proxy

import (
	"log"
	"net"
)

// handleUDPPacket forwards a single UDP packet to the target and sends back the response.
func handleUDPPacket(udpConn *net.UDPConn, clientAddr *net.UDPAddr, data []byte, target string) {
	// Resolve target address
	targetAddr, err := net.ResolveUDPAddr("udp", target)
	if err != nil {
		log.Printf("[UDP] resolve target %s error: %v", target, err)
		return
	}

	// Create a temporary connection to the target
	tmpConn, err := net.DialUDP("udp", nil, targetAddr)
	if err != nil {
		log.Printf("[UDP] dial to target %s error: %v", target, err)
		return
	}
	defer tmpConn.Close()

	// Send packet to target
	if _, err := tmpConn.Write(data); err != nil {
		log.Printf("[UDP] write to target error: %v", err)
		return
	}

	// Read response
	respBuf := make([]byte, 65535)
	n, _, err := tmpConn.ReadFromUDP(respBuf)
	if err != nil {
		log.Printf("[UDP] read from target error: %v", err)
		return
	}

	// Send response back to original client
	if _, err := udpConn.WriteToUDP(respBuf[:n], clientAddr); err != nil {
		log.Printf("[UDP] write back to client error: %v", err)
	}
}