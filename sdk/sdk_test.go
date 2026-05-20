package sdk

import (
	"context"
	"testing"
)

func TestSubmitTx(t *testing.T) {
	key := []byte("thisisaverysecretkey")
	client := NewRelayClient(key)

	tx := "test transaction"
	chainID := "test-chain"

	encryptedTx, err := client.SubmitTx(context.Background(), tx, chainID)
	if err != nil {
		t.Errorf("SubmitTx failed: %v", err)
	}

	decryptedTx, err := client.decrypt(encryptedTx)
	if err != nil {
		t.Errorf("decrypt failed: %v", err)
	}

	if decryptedTx != tx {
		t.Errorf("decrypted transaction does not match original: got %s, want %s", decryptedTx, tx)
	}
}