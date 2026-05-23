
package gpu

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/NVIDIA/nvidia-docker/cloud-provider/nvidia-gpu-plugin/client"
)

type GPU struct {
	ID      string
	Name    string
	Version string
}

func Discover() ([]GPU, error) {
	plugins, err := client.NewPluginClient().List()
	if err != nil {
		return nil, err
	}

	gpus := []GPU{}
	for _, plugin := range plugins {
		if strings.Contains(plugin.Name, "nvidia-container-runtime") {
			for _, device := range plugin.Devices {
				gpus = append(gpus, GPU{
					ID:      device.ID,
					Name:    device.Name,
					Version: device.Version,
				})
			}
		}
	}

	return gpus, nil
}

// opt/axentx/surrogate-1/pkg/gpu/types.go

package gpu

type GPU struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Version string `json:"version"`
}