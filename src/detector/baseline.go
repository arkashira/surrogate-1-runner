package detector

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/go-redis/redis/v8"
	"opt/axentx/surrogate-1/src/storage"
)

// redisBaseline implements BaselineRetriever using Redis.
type redisBaseline struct {
	client    storage.RedisClient // interface, not concrete type → mockable
	keyPrefix string              // defaults to "baseline:"
}

// NewRedisBaseline creates a BaselineRetriever backed by Redis.
func NewRedisBaseline(client storage.RedisClient) BaselineRetriever {
	return &redisBaseline{
		client:    client,
		keyPrefix: "baseline:",
	}
}

// GetBaseline fetches the JSON‑encoded slice of Signature stored under
// "<keyPrefix><service>" and unmarshals it.
func (r *redisBaseline) GetBaseline(ctx context.Context, service string) ([]Signature, error) {
	key := fmt.Sprintf("%s%s", r.keyPrefix, service)

	data, err := r.client.Get(ctx, key).Result()
	if err != nil {
		if err == redis.Nil {
			// No baseline yet – treat as empty.
			return []Signature{}, nil
		}
		return nil, fmt.Errorf("redis get baseline: %w", err)
	}

	var sigs []Signature
	if err := json.Unmarshal([]byte(data), &sigs); err != nil {
		return nil, fmt.Errorf("unmarshal baseline signatures: %w", err)
	}
	return sigs, nil
}