package main

import (
	"log"

	"github.com/axentx/surrogate-1/config"
	"github.com/axentx/surrogate-1/hipaa"
	"github.com/axentx/surrogate-1/soc2"
)

func main() {
	hipaaConfig := config.NewHIPAAConfig()
	soc2Config := config.NewSOC2Config()

	hipaa.Integrate(hipaaConfig)
	soc2.Integrate(soc2Config)

	log.Println("HIPAA and SOC2 integration completed.")
}