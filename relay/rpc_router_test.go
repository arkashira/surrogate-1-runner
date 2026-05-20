package relay

import (
	"context"
	"testing"

	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/stretchr/testify/assert"
)

func TestNewRPCRouter(t *testing.T) {
	router := NewRPCRouter()
	assert.NotNil(t, router)
}

func TestRouteRequest(t *testing.T) {
	router := NewRPCRouter()
	ctx := context.Background()

	resp, err := router.RouteRequest(ctx, 1, "eth_blockNumber", []interface{}{})
	assert.NoError(t, err)
	assert.NotNil(t, resp)
}

func TestSendTransaction(t *testing.T) {
	router := NewRPCRouter()
	ctx := context.Background()

	tx := types.NewTransaction(0, common.HexToAddress("0x0"), big.NewInt(0), 21000, big.NewInt(0), nil)
	receipt, err := router.SendTransaction(ctx, 1, tx)
	assert.NoError(t, err)
	assert.NotNil(t, receipt)
}

func TestGasPriceAdjustment(t *testing.T) {
	router := NewRPCRouter()
	chainID := uint64(1)
	config := router.chainConfigs[chainID]

	tx := types.NewTransaction(0, common.Address{}, big.NewInt(1000000000), 21000, big.NewInt(1000000000), nil)
	args := []interface{}{tx}

	receipt, err := router.SendTransaction(context.Background(), chainID, tx)
	assert.NoError(t, err)

	expectedGasPrice := config.GasPrice.ToInt()
	actualGasPrice := receipt.GasPrice()
	assert.Equal(t, expectedGasPrice, actualGasPrice)
}