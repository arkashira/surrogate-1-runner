package relay

import (
	"context"
	"fmt"
	"net/http"

	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/rpc"
)

type ChainConfig struct {
	RPCEndpoint string
	GasPrice    hexutil.Big
}

type RPCRouter interface {
	RouteRequest(ctx context.Context, chainID uint64, method string, args []interface{}) (*rpc.Response, error)
	SendTransaction(ctx context.Context, chainID uint64, tx *types.Transaction) (*types.Receipt, error)
}

type RPCRouterImpl struct {
	chainConfigs map[uint64]ChainConfig
}

func NewRPCRouter() RPCRouter {
	return &RPCRouterImpl{
		chainConfigs: map[uint64]ChainConfig{
			1:   {RPCEndpoint: "https://mainnet.infura.io/v3/YOUR_PROJECT_ID", GasPrice: hexutil.MustBigFromString("1000000000")},
			56:  {RPCEndpoint: "https://bsc-dataseed.binance.org/", GasPrice: hexutil.MustBigFromString("5000000000")},
			// Add more chains as needed
		},
	}
}

func (r *RPCRouterImpl) RouteRequest(ctx context.Context, chainID uint64, method string, args []interface{}) (*rpc.Response, error) {
	config, ok := r.chainConfigs[chainID]
	if !ok {
		return nil, fmt.Errorf("chain ID %d not supported", chainID)
	}

	client, err := rpc.DialContext(ctx, config.RPCEndpoint)
	if err != nil {
		return nil, err
	}
	defer client.Close()

	return client.CallContext(ctx, &rpc.Response{}, method, args...)
}

func (r *RPCRouterImpl) SendTransaction(ctx context.Context, chainID uint64, tx *types.Transaction) (*types.Receipt, error) {
	config, ok := r.chainConfigs[chainID]
	if !ok {
		return nil, fmt.Errorf("chain ID %d not supported", chainID)
	}

	client, err := rpc.DialContext(ctx, config.RPCEndpoint)
	if err != nil {
		return nil, err
	}
	defer client.Close()

	gasPrice := config.GasPrice.ToInt()
	tx.SetGasPrice(gasPrice)

	err = client.SendTransaction(ctx, tx)
	if err != nil {
		return nil, err
	}

	receipt, err := client.TransactionReceipt(ctx, tx.Hash())
	if err != nil {
		return nil, err
	}

	return receipt, nil
}

func HandleRPCRequest(w http.ResponseWriter, r *http.Request) {
	// Example handler, replace with actual implementation
	chainID := uint64(1) // Extract chainID from request
	method := "eth_sendTransaction" // Extract method from request
	args := []interface{}{} // Extract args from request

	router := NewRPCRouter()
	resp, err := router.SendTransaction(r.Context(), chainID, args[0].(*types.Transaction))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(resp)
}