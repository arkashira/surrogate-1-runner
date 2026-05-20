package multiplexing

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
)

// VMEntry represents a single internal VM and its associated NAT endpoint.
type VMEntry struct {
	VMIP    string `json:"vm_ip"`
	NATIP   string `json:"nat_ip"`
	NATPort int    `json:"nat_port"`
}

// VMConfig holds all VM entries for the multiplexed NAT configuration.
type VMConfig struct {
	Entries []VMEntry `json:"entries"`
}

// ConfigureVMs writes a JSON configuration file that maps each internal VM
// to the multiplexed NAT endpoint. The configuration is written to the
// specified output path. The VMs can read this file (e.g. via a shared
// volume) to discover the NAT IP/port without any client‑side software.
func ConfigureVMs(natIP string, natPort int, vmIPs []string, outputPath string) error {
	if natIP == "" {
		return fmt.Errorf("natIP cannot be empty")
	}
	if natPort <= 0 || natPort > 65535 {
		return fmt.Errorf("invalid natPort: %d", natPort)
	}
	if len(vmIPs) == 0 {
		return fmt.Errorf("no vmIPs provided")
	}

	entries := make([]VMEntry, 0, len(vmIPs))
	for _, ip := range vmIPs {
		entries = append(entries, VMEntry{
			VMIP:    ip,
			NATIP:   natIP,
			NATPort: natPort,
		})
	}

	cfg := VMConfig{Entries: entries}
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal config: %w", err)
	}

	// Ensure directory exists
	dir := filepath.Dir(outputPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create config dir %s: %w", dir, err)
	}

	if err := ioutil.WriteFile(outputPath, data, 0644); err != nil {
		return fmt.Errorf("failed to write config file %s: %w", outputPath, err)
	}
	return nil
}