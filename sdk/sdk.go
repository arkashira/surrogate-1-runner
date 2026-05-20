
package sdk

import (
	"context"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/url"
	"sync"

	"github.com/gorilla/websocket"
)

type RelayClient struct {
	url      *url.URL
	client   *websocket.Conn
	encrypt  func(data []byte) ([]byte, error)
	decrypt  func(data []byte) ([]byte, error)
	receipt  chan Receipt
	receiptW sync.WaitGroup
}

func NewRelayClient(url string, key string) (*RelayClient, error) {
	// Initialize the URL and create the WebSocket connection
	u, err := url.Parse(url)
	if err != nil {
		return nil, err
	}

	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		return nil, err
	}

	// Generate the encryption key and create the encrypt and decrypt functions
	block, _ := aes.NewCipher([]byte(key))
	encrypt := func(data []byte) ([]byte, error) {
		// Encrypt the data using AES-256-CBC with a random IV
		gcm, err := cipher.NewGCM(block)
		if err != nil {
			return nil, err
		}
		nonce := make([]byte, gcm.NonceSize())
		if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
			return nil, err
		}
		ciphertext := gcm.Encrypt(nonce, nonce, data, nil)
		return ciphertext, nil
	}
	decrypt := func(data []byte) ([]byte, error) {
		// Decrypt the data using AES-256-CBC with the same IV as the encrypted data
		gcm, err := cipher.NewGCM(block)
		if err != nil {
			return nil, err
		}
		nonce := data[:gcm.NonceSize()]
		ciphertext := data[gcm.NonceSize():]
		plaintext, err := gcm.Decrypt(nonce, nonce, ciphertext, nil)
		return plaintext, err
	}

	return &RelayClient{
		url:      u,
		client:   c,
		encrypt:  encrypt,
		decrypt:  decrypt,
		receipt:  make(chan Receipt),
	}, nil
}

func (c *RelayClient) SubmitTx(ctx context.Context, tx []byte, chainID string) error {
	// Encrypt the transaction payload and send it to the WebSocket connection
	encryptedTx, err := c.encrypt(tx)
	if err != nil {
		return err
	}

	err = c.client.WriteMessage(websocket.TextMessage, encryptedTx)
	if err != nil {
		return err
	}

	// Start a goroutine to handle the receipt subscription
	c.receiptW.Add(1)
	go func() {
		defer c.receiptW.Done()
		for receipt := range c.receipt {
			// Handle the receipt here
			fmt.Println("Received receipt:", receipt)
		}
	}()

	return nil
}

func (c *RelayClient) OnReceipt(callback func(Receipt)) {
	// Subscribe to the receipt channel and call the callback function when a receipt is received
	c.receipt = make(chan Receipt, 10)
	go func() {
		defer close(c.receipt)
		for receipt := range c.client.ReadChannel(websocket.TextMessage) {
			c.receipt <- receipt
			callback(receipt)
		}
	}()
}

// Wait waits for all goroutines started by OnReceipt to finish
func (c *RelayClient) Wait() {
	c.receiptW.Wait()
}

// Receipt is the structure of a receipt message
type Receipt struct {
	ChainID string `json:"chain_id"`
	Hash    string `json:"hash"`
}