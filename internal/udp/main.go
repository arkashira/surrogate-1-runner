package main

import (
	"log"
	"os"

	"github.com/spf13/viper"
	"github.com/axentx/surrogate-1/internal/udp"
)

func initConfig() {
	viper.SetConfigName("keep")
	viper.AddConfigPath("/etc/axentx/")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file, %s", err)
	}
}

func main() {
	initConfig()

	port := viper.GetInt("udp_port")
	if port == 0 {
		port = 40000
	}

	listener, err := udp.NewListener(port)
	if err != nil {
		log.Fatalf("Failed to create UDP listener: %v", err)
	}
	defer listener.Close()

	log.Printf("KEEP listening on UDP port %d", port)

	select {}
}