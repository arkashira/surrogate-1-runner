package auth

import (
	"errors"
	"fmt"
)

var (
	users = make(map[string]User)
)

type User struct {
	ID       string
	Username string
	Password string
}

func CreateUser(id, username, password string) error {
	if _, exists := users[id]; exists {
		return errors.New("user already exists")
	}

	users[id] = User{
		ID:       id,
		Username: username,
		Password: password,
	}

	fmt.Printf("Created user: %+v\n", users[id])
	return nil
}