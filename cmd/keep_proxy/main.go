package main

import (
	"context"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/axentx/surrogate-1/tcp_dispatcher"
	"github.com/axentx/surrogate-1/udp_multiplexer"
)

func startTCPListener(ctx context.Context) error {
	listener, err := net.Listen("tcp", ":443")
	if err != nil {
		return fmt.Errorf("failed to listen on TCP port 443: %w", err)
	}
	defer listener.Close()

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				fmt.Printf("Failed to accept TCP connection: %v\n", err)
				continue
			}
			go tcp_dispatcher.Dispatch(conn)
		}
	}()

	<-ctx.Done()
	return nil
}

func startUDPListener(ctx context.Context) error {
	addr, err := net.ResolveUDPAddr("udp", ":40000")
	if err != nil {
		return fmt.Errorf("failed to resolve UDP address: %w", err)
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		return fmt.Errorf("failed to listen on UDP port 40000: %w", err)
	}
	defer conn.Close()

	go udp_multiplexer.Multiplex(conn)

	<-ctx.Done()
	return nil
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	http.HandleFunc("/healthz", healthCheckHandler)
	go http.ListenAndServe(":8080", nil)

	tcpCtx, tcpCancel := context.WithTimeout(ctx, 2*time.Second)
	defer tcpCancel()
	if err := startTCPListener(tcpCtx); err != nil {
		fmt.Printf("Failed to start TCP listener: %v\n", err)
		os.Exit(1)
	}

	udpCtx, udpCancel := context.WithTimeout(ctx, 2*time.Second)
	defer udpCancel()
	if err := startUDPListener(udpCtx); err != nil {
		fmt.Printf("Failed to start UDP listener: %v\n", err)
		os.Exit(1)
	}

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	fmt.Println("Shutting down gracefully...")
	ctx, cancel = context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	startTCPListener(ctx)
	startUDPListener(ctx)
}