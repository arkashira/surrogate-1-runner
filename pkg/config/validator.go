package config

import (
	"fmt"
	"reflect"

	"github.com/go-playground/validator/v10"
	"github.com/spf13/viper"
)

type ServiceMapping struct {
	Protocol string `mapstructure:"protocol" validate:"required,oneof=TCP UDP"`
	Port     int    `mapstructure:"port" validate:"required"`
	Internal string `mapstructure:"internal" validate:"required"`
}

func ValidateConfig(config map[string]interface{}) error {
	v := viper.New()
	v.SetConfigType("yaml")
	err := v.ReadConfig(config)
	if err != nil {
		return err
	}

	err = v.Unmarshal(&config)
	if err != nil {
		return err
	}

	if err := validator.New().Struct(config); err != nil {
		return fmt.Errorf("invalid config: %w", err)
	}

	return nil
}

func ValidateServiceMapping(mapping ServiceMapping) error {
	if err := validator.New().Struct(mapping); err != nil {
		return fmt.Errorf("invalid service mapping: %w", err)
	}

	return nil
}