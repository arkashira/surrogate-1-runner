package scanner

import (
	"strings"

	"github.com/hashicorp/terraform-config-inspect/tfconfig"
	"github.com/hashicorp/terraform-config-inspect/tfconfig/ast"
)

func ScanTerraform(config *tfconfig.Config) []string {
	var vulnerabilities []string

	for _, module := range config.Modules {
		for _, resource := range module.Resources {
			if strings.Contains(resource.Type, "aws_instance") && !strings.Contains(resource.Attributes["instance_type"], "t2.micro") {
				vulnerabilities = append(vulnerabilities, "Potential cost issue: Non-t2.micro instance type used - "+resource.Address)
			}
			if strings.Contains(resource.Type, "aws_security_group") && !strings.Contains(resource.Attributes["name"], "allow_all") {
				vulnerabilities = append(vulnerabilities, "Security risk: Security group does not allow all traffic - "+resource.Address)
			}
		}
	}

	return vulnerabilities
}