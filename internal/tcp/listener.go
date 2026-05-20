package tcp

import (
	"net"
)

type Listener struct {
	Addr string
	Conn net.Listener
}