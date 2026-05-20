package repo

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/axentx/surrogate-1/internal/config"
)

type Repo struct {
	Name string
	Files []string
}

func GetRepos() (map[string]*Repo, error) {
	repos := make(map[string]*Repo)

	// Assuming repos are stored in a database or file system
	// and can be retrieved by name

	return repos, nil
}