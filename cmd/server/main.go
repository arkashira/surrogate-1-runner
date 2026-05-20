package main

import (
	"log"

	"opt/axentx/surrogate-1/pkg/server"
)

func main() {
	// In production you would read the bind address from a flag or env var.
	const bindAddr = ":8080"

	if err := server.Start(bindAddr); err != nil {
		log.Fatalf("server stopped with error: %v", err)
	}
}