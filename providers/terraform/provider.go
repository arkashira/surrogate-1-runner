package terraform

import (
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
	"opt/axentx/surrogate-1/providers/terraform/resources"
)

func Provider() *schema.Provider {
	return &schema.Provider{
		ResourcesMap: map[string]*schema.Resource{
			"surrogate_workflow": resources.resourceWorkflow(),
		},
	}
}