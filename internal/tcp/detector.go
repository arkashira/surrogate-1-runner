
package tcp

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

type ProtocolDetector struct {
	snis map[string]func(net.Conn)
	alpns map[string]func(net.Conn)
	banners map[string]func(net.Conn)
	timeout time.Duration
	mu sync.Mutex
}

func NewProtocolDetector() *ProtocolDetector {
	pd := &ProtocolDetector{
		snis: make(map[string]func(net.Conn)),
		alpns: make(map[string]func(net.Conn)),
		banners: make(map[string]func(net.Conn)),
		timeout: 2 * time.Second,
	}

	// Add your custom protocol detection functions here

	return pd
}

func (pd *ProtocolDetector) Detect(conn net.Conn) {
	defer conn.Close()

	reader := bufio.NewReader(conn)

	select {
	case <-time.After(pd.timeout):
		conn.Write([]byte("HTTP/1.1 421 Unable to route\r\n\r\n"))
		return
	case sni := <-pd.detectSNI(reader):
		sni(conn)
	case alpn := <-pd.detectALPN(reader):
		alpn(conn)
	case banner := <-pd.detectBanner(reader):
		banner(conn)
	}
}

func (pd *ProtocolDetector) detectSNI(reader *bufio.Reader) chan string {
	go func() {
		line, err := reader.ReadString('\n')
		if err != nil {
			return
		}

		line = strings.TrimSpace(line)
		pd.mu.Lock()
		for sni, handler := range pd.snis {
			if strings.HasPrefix(line, sni) {
				pd.mu.Unlock()
				pd.snis[sni](conn)
				return
			}
		}
		pd.mu.Unlock()
	}()

	return make(chan string)
}

func (pd *ProtocolDetector) detectALPN(reader *bufio.Reader) chan string {
	go func() {
		line, err := reader.ReadString('\n')
		if err != nil {
			return
		}

		line = strings.TrimSpace(line)
		pd.mu.Lock()
		for alpn, handler := range pd.alpns {
			if strings.HasPrefix(line, alpn) {
				pd.mu.Unlock()
				pd.alpns[alpn](conn)
				return
			}
		}
		pd.mu.Unlock()
	}()

	return make(chan string)
}

func (pd *ProtocolDetector) detectBanner(reader *bufio.Reader) chan string {
	go func() {
		line, err := reader.ReadString('\n')
		if err != nil {
			return
		}

		line = strings.TrimSpace(line)
		pd.mu.Lock()
		for banner, handler := range pd.banners {
			if strings.HasPrefix(line, banner) {
				pd.mu.Unlock()
				pd.banners[banner](conn)
				return
			}
		}
		pd.mu.Unlock()
	}()

	return make(chan string)
}