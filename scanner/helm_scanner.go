package scanner

import (
	"strings"

	"helm.sh/helm/v3/pkg/chart"
)

func ScanHelm(chart *chart.Chart) []string {
	var vulnerabilities []string

	for _, file := range chart.Files {
		if strings.Contains(file.Name, "values.yaml") {
			if strings.Contains(file.Data, "replicaCount: 1") {
				vulnerabilities = append(vulnerabilities, "Potential availability issue: Replica count set to 1 - "+file.Name)
			}
			if strings.Contains(file.Data, "image: nginx:latest") {
				vulnerabilities = append(vulnerabilities, "Security risk: Using latest tag for container image - "+file.Name)
			}
		}
	}

	return vulnerabilities
}