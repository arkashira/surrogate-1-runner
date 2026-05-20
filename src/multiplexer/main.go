package main

import (
	"log"

	"github.com/axentx/surrogate-1/pkg/multiplexer"
)

func main() {
	listener, err := multiplexer.NewUDPListener(1234)
	if err != nil {
		log.Fatal(err)
	}
	listener.Start()
}