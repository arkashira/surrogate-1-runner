package main

import (
	"context"
	"log"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"opt/axentx/surrogate-1/api/fd"
	"opt/axentx/surrogate-1/internal/fd"

	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/emptypb"
)

const (
	grpcAddr   = "0.0.0.0:50051"
	healthAddr = "0.0.0.0:8080"
)

// server implements the generated FDServiceServer interface.
type server struct {
	fd.UnimplementedFDServiceServer
}

// ListFDs fulfills the gRPC request by delegating to the internal library.
func (s *server) ListFDs(ctx context.Context, _ *emptypb.Empty) (*fd.ListFDsResponse, error) {
	fds, err := fd.ListOpenFDs()
	if err != nil {
		return nil, err
	}

	resp := &fd.ListFDsResponse{}
	for _, info := range fds {
		resp.Fds = append(resp.Fds, &fd.FDInfo{
			Fd:     info.FD,
			Target: info.Target,
			Type:   info.Type,
		})
	}
	return resp, nil
}

// healthHandler returns a simple 200 OK for /healthz.
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("OK"))
}

func main() {
	// Set up signal handling for graceful shutdown.
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	// ---------- gRPC server ----------
	lis, err := net.Listen("tcp", grpcAddr)
	if err != nil {
		log.Fatalf("failed to listen on %s: %v", grpcAddr, err)
	}
	grpcServer := grpc.NewServer()
	fd.RegisterFDServiceServer(grpcServer, &server{})

	// Run gRPC server in background.
	go func() {
		log.Printf("gRPC server listening on %s", grpcAddr)
		if err := grpcServer.Serve(lis); err != nil && err != grpc.ErrServerStopped {
			log.Fatalf("gRPC server error: %v", err)
		}
	}()

	// ---------- HTTP health server ----------
	httpMux := http.NewServeMux()
	httpMux.HandleFunc("/healthz", healthHandler)

	httpServer := &http.Server{
		Addr:    healthAddr,
		Handler: httpMux,
	}

	go func() {
		log.Printf("Health endpoint listening on %s", healthAddr)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Health server error: %v", err)
		}
	}()

	// Wait for termination signal.
	<-ctx.Done()
	log.Println("Shutdown signal received, stopping servers...")

	grpcServer.GracefulStop()
	if err := httpServer.Shutdown(context.Background()); err != nil {
		log.Printf("HTTP server shutdown error: %v", err)
	}
	log.Println("Sidecar stopped cleanly")
}