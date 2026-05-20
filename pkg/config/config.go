package config

import (
	"fmt"
	"log"
	"os"
	"sync"

	"github.com/go-playground/validator/v10"
	"github.com/spf13/viper"
)

var (
	once sync.Once
	v    *viper.Viper
)

func GetConfig() (*viper.Viper, error) {
	once.Do(func() {
		v = viper.New()
		v.SetConfigType("yaml")
		v.SetConfigFile("/opt/axentx/surrogate-1/config/config.yaml")
		err := v.ReadInConfig()
		if err != nil {
			log.Fatal(err)
		}
	})

	return v, nil
}

func LoadConfig() error {
	v, err := GetConfig()
	if err != nil {
		return err
	}

	err = v.Unmarshal(&config)
	if err != nil {
		return err
	}

	return nil
}

func UpdateConfig() error {
	v, err := GetConfig()
	if err != nil {
		return err
	}

	err = v.Unmarshal(&config)
	if err != nil {
		return err
	}

	return nil
}