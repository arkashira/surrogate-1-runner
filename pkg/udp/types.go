package udp

type UDPMapping struct {
	PublicPort      string `yaml:"public_port"`
	InternalEndpoint string `yaml:"internal_endpoint"`
	Description     string `yaml:"description"`
}