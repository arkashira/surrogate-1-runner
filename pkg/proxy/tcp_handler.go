package proxy

import (
	"io"
	"log"
	"net"
)

// handleTCPConnection forwards a single TCP connection to the target.
// It copies data bidirectionally until EOF or error.
func handleTCPConnection(src net.Conn, target string) {
	defer src.Close()
	dst, err := net.Dial("tcp", target)
	if err != nil {
		log.Printf("[TCP] dial to %s failed: %v", target, err)
		return
	}
	defer dst.Close()

	// Bidirectional copy
	var wg sync.WaitGroup
	wg.Add(2)

	go func() {
		defer wg.Done()
		if _, err := io.Copy(dst, src); err != nil {
			log.Printf("[TCP] copy src->dst error: %v", err)
		}
		dst.(*net.TCPConn).CloseWrite()
	}()

	go func() {
		defer wg.Done()
		if _, err := io.Copy(src, dst); err != nil {
			log.Printf("[TCP] copy dst->src error: %v", err)
		}
		src.(*net.TCPConn).CloseWrite()
	}()

	wg.Wait()
}