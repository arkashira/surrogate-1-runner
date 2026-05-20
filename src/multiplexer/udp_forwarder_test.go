package multiplexer

import (
	"net"
	"testing"
	"time"
)

func TestUDPMultiplexer(t *testing.T) {
	// Test 1: Verify source IP preservation
	mux, _ := NewUDPMultiplexer(12345, "127.0.0.1:54321")
	go mux.Start()
	
	// Create test packet with known source
	testPacket := []byte("NAT test payload")
	srcAddr, _ := net.ResolveUDPAddr("udp", "192.168.1.100:65432")
	
	// Simulate incoming packet
	mux.listener.WriteToUDP(testPacket, srcAddr.(*net.UDPAddr))
	
	// Verify received packet preserves source
	time.Sleep(100 * time.Millisecond)
	// (Add actual verification logic here)
	
	// Test 2: Verify packet drop when no mapping
	mux.mu.Lock()
	mux.mappingExists = false
	mux.mu.Unlock()
	
	mux.listener.WriteToUDP(testPacket, srcAddr.(*net.UDPAddr))
	
	// Verify metric counter incremented
	// (Add metric verification logic here)
}