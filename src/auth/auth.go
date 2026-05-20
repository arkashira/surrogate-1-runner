package auth

import (
	"encoding/json"
	"fmt"
	"os"
)

type Auth struct {
	Mappings map[string]int
	Token    string
}

func GetStaticToken() string {
	return os.Getenv("STATIC_TOKEN")
}

func GetMappings() Mappings {
	return Mappings{Mappings: auth.Mappings}
}

func AddMapping(service string, port int) {
	auth.Mappings[service] = port
}

func DeleteMapping(service string) {
	delete(auth.Mappings, service)
}

func NewAuthMiddleware() *AuthMiddleware {
	return &AuthMiddleware{}
}