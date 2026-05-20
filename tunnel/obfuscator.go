package tunnel

import (
	"crypto/rand"
	"crypto/tls"
	"io"
	"net"
	"time"
)

// Obfuscator wraps a raw net.Conn with a custom handshake and
// XOR‑based payload obfuscation while preserving end‑to‑end TLS encryption.
type Obfuscator struct {
	rawConn net.Conn
	tlsConn *tls.Conn
}

// NewObfuscator performs a lightweight custom handshake (exchange of
// 16‑byte random masks) and then upgrades the connection to TLS.
// The caller provides a *tls.Config appropriate for the target server.
func NewObfuscator(rawConn net.Conn, cfg *tls.Config) (*Obfuscator, error) {
	// ---- custom handshake -------------------------------------------------
	// client sends a 16‑byte random mask
	clientMask := make([]byte, 16)
	if _, err := rand.Read(clientMask); err != nil {
		return nil, err
	}
	if _, err := rawConn.Write(clientMask); err != nil {
		return nil, err
	}

	// read server mask (must be exactly 16 bytes)
	serverMask := make([]byte, 16)
	if _, err := io.ReadFull(rawConn, serverMask); err != nil {
		return nil, err
	}
	// In a real implementation the two masks would be combined into a
	// shared secret. For this prototype we simply continue.

	// ---- TLS upgrade -------------------------------------------------------
	tlsConn := tls.Client(rawConn, cfg)
	if err := tlsConn.Handshake(); err != nil {
		return nil, err
	}

	return &Obfuscator{
		rawConn: rawConn,
		tlsConn: tlsConn,
	}, nil
}

// Read reads from the TLS connection, then de‑obfuscates the payload.
func (o *Obfuscator) Read(b []byte) (int, error) {
	n, err := o.tlsConn.Read(b)
	if n > 0 {
		xor(b[:n])
	}
	return n, err
}

// Write obfuscates the payload before writing it to the TLS connection.
func (o *Obfuscator) Write(b []byte) (int, error) {
	tmp := make([]byte, len(b))
	copy(tmp, b)
	xor(tmp)
	return o.tlsConn.Write(tmp)
}

// Close closes the underlying TLS connection.
func (o *Obfuscator) Close() error {
	return o.tlsConn.Close()
}

// LocalAddr returns the local network address.
func (o *Obfuscator) LocalAddr() net.Addr { return o.tlsConn.LocalAddr() }

// RemoteAddr returns the remote network address.
func (o *Obfuscator) RemoteAddr() net.Addr { return o.tlsConn.RemoteAddr() }

// SetDeadline sets the read and write deadlines associated with the connection.
func (o *Obfuscator) SetDeadline(t time.Time) error {
	return o.tlsConn.SetDeadline(t)
}

// SetReadDeadline sets the deadline for future Read calls.
func (o *Obfuscator) SetReadDeadline(t time.Time) error {
	return o.tlsConn.SetReadDeadline(t)
}

// SetWriteDeadline sets the deadline for future Write calls.
func (o *Obfuscator) SetWriteDeadline(t time.Time) error {
	return o.tlsConn.SetWriteDeadline(t)
}

// xor applies a simple static XOR to the supplied byte slice.
// In production this would be replaced by a proper stream cipher derived
// from the handshake secret.
func xor(data []byte) {
	const key = byte(0xAA)
	for i := range data {
		data[i] ^= key
	}
}