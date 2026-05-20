package multiplexer

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"strconv"

	"github.com/axentx/surrogate-1/config"
)

// TCPListener represents a TCP listener
type TCPListener struct {
	Port int
}

// NewTCPListener returns a new TCP listener
func NewTCPListener(port int) *TCPListener {
	return &TCPListener{Port: port}
}

// Listen starts the TCP listener
func (t *TCPListener) Listen() error {
	log.Printf("Starting TCP listener on port %d\n", t.Port)
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(t.Port))
	if err != nil {
		return err
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		go t.handleConnection(conn)
	}
}

func (t *TCPListener) handleConnection(conn net.Conn) {
	// Handle incoming connection
	log.Printf("New connection from %s\n", conn.RemoteAddr())
	// TO DO: implement connection routing logic
}

func main() {
	// Load configuration
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	// Create a new TCP listener
	listener := NewTCPListener(cfg.Port)

	// Start the TCP listener
	if err := listener.Listen(); err != nil {
		log.Fatal(err)
	}
}