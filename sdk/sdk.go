package sdk

import (
	"context"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"errors"
)

type RelayClient struct {
	encryptionKey []byte
}

func NewRelayClient(encryptionKey []byte) *RelayClient {
	return &RelayClient{encryptionKey: encryptionKey}
}

func (rc *RelayClient) SubmitTx(ctx context.Context, tx string, chainID string) (string, error) {
	encryptedTx, err := rc.encrypt(tx)
	if err != nil {
		return "", err
	}
	// Simulate submission of encrypted transaction
	return encryptedTx, nil
}

func (rc *RelayClient) OnReceipt(callback func(string)) {
	// Placeholder for receipt subscription logic
}

func (rc *RelayClient) encrypt(plaintext string) (string, error) {
	block, err := aes.NewCipher(rc.encryptionKey)
	if err != nil {
		return "", err
	}

	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	if _, err := rand.Read(iv); err != nil {
		return "", err
	}

	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], []byte(plaintext))

	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func (rc *RelayClient) decrypt(ciphertext string) (string, error) {
	data, err := base64.StdEncoding.DecodeString(ciphertext)
	if err != nil {
		return "", err
	}

	block, err := aes.NewCipher(rc.encryptionKey)
	if err != nil {
		return "", err
	}

	if len(data) < aes.BlockSize {
		return "", errors.New("ciphertext too short")
	}

	iv := data[:aes.BlockSize]
	data = data[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	stream.XORKeyStream(data, data)

	return string(data), nil
}