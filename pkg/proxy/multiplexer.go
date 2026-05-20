package proxy

import (
	"log"
	"net"
	"sync"
)

// Mapping defines the external port to internal target mapping.
// The target is a string in the form "host:port".
type Mapping map[int]string

// Multiplexer multiplexes TCP and UDP traffic on a single public IP/port
// and forwards it to internal services based on the Mapping.
type Multiplexer struct {
	PublicAddr string   // e.g. ":8080" or "0.0.0.0:8080"
	TCPMap     Mapping  // external TCP port -> internal target
	UDPMap     Mapping  // external UDP port -> internal target
	wg         sync.WaitGroup
}

// NewMultiplexer creates a new Multiplexer instance.
func NewMultiplexer(publicAddr string, tcpMap, udpMap Mapping) *Multiplexer {
	return &Multiplexer{
		PublicAddr: publicAddr,
		TCPMap:     tcpMap,
		UDPMap:     udpMap,
	}
}

// Start begins listening for TCP and UDP traffic and forwards it.
// It blocks until all listeners are closed (which never happens in this simple example).
func (m *Multiplexer) Start() error {
	// Start TCP listener
	tcpListener, err := net.Listen("tcp", m.PublicAddr)
	if err != nil {
		return err
	}
	m.wg.Add(1)
	go func() {
		defer m.wg.Done()
		m.handleTCP(tcpListener)
	}()

	// Start UDP listener
	udpAddr, err := net.ResolveUDPAddr("udp", m.PublicAddr)
	if err != nil {
		return err
	}
	udpConn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		return err
	}
	m.wg.Add(1)
	go func() {
		defer m.wg.Done()
		m.handleUDP(udpConn)
	}()

	// Wait forever (or until context cancellation in a real implementation)
	m.wg.Wait()
	return nil
}

// handleTCP accepts connections and forwards them based on the TCPMap.
func (m *Multiplexer) handleTCP(listener net.Listener) {
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("[TCP] accept error: %v", err)
			continue
		}
		// Determine target based on remote port
		remotePort := conn.RemoteAddr().(*net.TCPAddr).Port
		target, ok := m.TCPMap[remotePort]
		if !ok {
			log.Printf("[TCP] no mapping for port %d, closing connection", remotePort)
			conn.Close()
			continue
		}
		go handleTCPConnection(conn, target)
	}
}

// handleUDP reads packets and forwards them based on the UDPMap.
func (m *Multiplexer) handleUDP(conn *net.UDPConn) {
	buf := make([]byte, 65535)
	for {
		n, clientAddr, err := conn.ReadFromUDP(buf)
		if err != nil {
			log.Printf("[UDP] read error: %v", err)
			continue
		}
		// Determine target based on client port
		target, ok := m.UDPMap[clientAddr.Port]
		if !ok {
			log.Printf("[UDP] no mapping for port %d, dropping packet", clientAddr.Port)
			continue
		}
		go handleUDPPacket(conn, clientAddr, buf[:n], target)
	}
}