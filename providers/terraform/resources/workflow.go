package resources

import (
	"context"
	"log"

	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

// resourceWorkflow defines the Terraform resource for a surrogate workflow.
// It supports basic CRUD operations and logs each action. The actual
// interaction with the surrogate backend is omitted for brevity and
// replaced with placeholder logic.
func resourceWorkflow() *schema.Resource {
	return &schema.Resource{
		CreateContext: resourceWorkflowCreate,
		ReadContext:   resourceWorkflowRead,
		UpdateContext: resourceWorkflowUpdate,
		DeleteContext: resourceWorkflowDelete,
		Schema: map[string]*schema.Schema{
			"name": {
				Type:     schema.TypeString,
				Required: true,
			},
			"steps": {
				Type:     schema.TypeList,
				Required: true,
				Elem: &schema.Schema{
					Type: schema.TypeString,
				},
			},
			"enabled": {
				Type:     schema.TypeBool,
				Optional: true,
				Default:  true,
			},
			// The following attribute is computed and returned by the
			// surrogate backend after workflow creation.
			"id": {
				Type:     schema.TypeString,
				Computed: true,
			},
		},
	}
}

func resourceWorkflowCreate(ctx context.Context, d *schema.ResourceData, m interface{}) diag.Diagnostics {
	// In a real implementation, this would call the surrogate API to
	// create a workflow and return its ID. Here we simply log and set
	// a dummy ID.
	name := d.Get("name").(string)
	log.Printf("[INFO] Creating workflow: %s", name)
	d.SetId(name) // use name as a stable ID for demo purposes
	return resourceWorkflowRead(ctx, d, m)
}

func resourceWorkflowRead(ctx context.Context, d *schema.ResourceData, m interface{}) diag.Diagnostics {
	// In a real implementation, this would fetch the workflow state
	// from the surrogate backend. For demo purposes, we assume the
	// workflow exists and nothing changes.
	return nil
}

func resourceWorkflowUpdate(ctx context.Context, d *schema.ResourceData, m interface{}) diag.Diagnostics {
	if d.HasChanges("steps", "enabled") {
		log.Printf("[INFO] Updating workflow %s", d.Id())
	}
	return resourceWorkflowRead(ctx, d, m)
}

func resourceWorkflowDelete(ctx context.Context, d *schema.ResourceData, m interface{}) diag.Diagnostics {
	log.Printf("[INFO] Deleting workflow %s", d.Id())
	d.SetId("")
	return nil
}