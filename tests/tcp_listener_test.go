package multiplexer

import (
	"net"
	"testing"
)

func TestTCPListener(t *testing.T) {
	// Create a new TCP listener
	listener := NewTCPListener(8080)

	// Start the TCP listener
	go func() {
		if err := listener.Listen(); err != nil {
			t.Fatal(err)
		}
	}()

	// Connect to the TCP listener
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		t.Fatal(err)
	}
	defer conn.Close()

	// Send a message to the TCP listener
	_, err = conn.Write([]byte("Hello, world!"))
	if err != nil {
		t.Fatal(err)
	}

	// Close the connection
	conn.Close()
}

func TestTCPListenerHandleConnection(t *testing.T) {
	// Create a new TCP listener
	listener := NewTCPListener(8080)

	// Start the TCP listener
	go func() {
		if err := listener.Listen(); err != nil {
			t.Fatal(err)
		}
	}()

	// Connect to the TCP listener
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		t.Fatal(err)
	}
	defer conn.Close()

	// Send a message to the TCP listener
	_, err = conn.Write([]byte("Hello, world!"))
	if err != nil {
		t.Fatal(err)
	}

	// Close the connection
	conn.Close()
}