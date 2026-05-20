package relay

import (
	"errors"
	"log"
)

var (
	// Whitelist of supported chain IDs
	supportedChains = map[string]bool{
		"1":   true, // Ethereum Mainnet
		"56":  true, // Binance Smart Chain
		"137": true, // Polygon
	}
)

// ValidateChainID checks if the provided chain ID is in the whitelist.
func ValidateChainID(chainID string) error {
	if _, exists := supportedChains[chainID]; !exists {
		return errors.New("unknown chain ID")
	}
	log.Printf("Routing transaction to chain ID: %s", chainID)
	return nil
}

// RouteTransaction routes the transaction based on the validated chain ID.
func RouteTransaction(chainID string) error {
	err := ValidateChainID(chainID)
	if err != nil {
		return err
	}
	// Logic to route the transaction to the correct network
	log.Printf("Transaction routed successfully to chain ID: %s", chainID)
	return nil
}